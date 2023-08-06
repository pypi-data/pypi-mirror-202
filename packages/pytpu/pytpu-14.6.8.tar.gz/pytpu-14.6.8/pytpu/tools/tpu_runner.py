import asyncio
import json
import logging
import os
import shutil
import tempfile

from math import ceil
from typing import Any
from typing import Dict
from typing import Tuple
from zipfile import ZipFile

import numpy as np

from tpu_tlm_is.base import TensorDescription
from tpu_tlm_is.base.number_types import UserNumberType
from tpu_tlm_is.base.number_types import TpuNumberType
from tpu_tlm_is.base.number_types import STR_TO_USER_NUMBER_TYPE
from tpu_tlm_is.base.number_types import STR_TO_TPU_NUMBER_TYPE
from tpu_tlm_is.models.iotools import post_process
from tpu_tlm_is.models.iotools import pre_process
from pytpu.pytpu import TPUDevice, TPUProgram, TPUInference  # type: ignore
from pytpu.pytpu import TPUProcessingMode
from pytpu.pytpu import load_inference
from pytpu.pytpu import get_inference
from pytpu.pytpu import submit_inference
from ..tools.helpers import get_tpu_devices
from ..tools.helpers import get_tpu_parameters
from ..tools.helpers import to_raw


__all__ = [
    'TpuRunner',
]

LOGGER = logging.getLogger(__name__)
_SUFFIX = ':0'


def _get_tensor_description(io_: Dict[str, Any], cwl: int) -> TensorDescription:
    if 'user_shape' in io_.keys():
        LOGGER.debug('Generate NON-RAW descriptions')
        return TensorDescription(
            user_shape_mask=tuple(tuple([True, ] * abs(p[0]) + [False, ] * s + [True, ] * abs(p[1])
                                  for p, s in zip(io_['padding'], io_['user_shape']))),
            user_order=io_['user_order'],
            user_dtype=STR_TO_USER_NUMBER_TYPE[io_['user_dtype']],
            tpu_shape=io_['tpu_shape'],
            tpu_order=io_['tpu_order'],
            tpu_dtype=STR_TO_TPU_NUMBER_TYPE[io_['tpu_dtype']],
            scales=tuple([float(s) for s in io_['scales']]),
            anchor=io_['anchor'],
        )
    else:
        LOGGER.debug('Generate RAW descriptions')
        return TensorDescription(
            user_shape_mask=((False, ), tuple([False, ] * int(io_['size'])), ),
            user_order=('N', 'C', ),
            user_dtype=UserNumberType.INT8,
            tpu_shape=(1, ceil(int(io_['size']) / cwl), np.minimum(cwl, int(io_['size']))),
            tpu_order=('N', 'C', 'B'),
            tpu_dtype=TpuNumberType.INT8,
            scales=(1.0, ),
        )


def _tensor_as_node(node: Dict[str, np.ndarray]) -> Tuple[Dict[str, np.ndarray], bool]:
    node_tensor = {}
    _len_suffix = len(_SUFFIX)
    flag_suffix = False
    for key, data in node.items():
        if key[-_len_suffix:] == _SUFFIX:
            node_tensor[key[:-_len_suffix]] = data
            flag_suffix = True
        else:
            node_tensor[key] = data
    return node_tensor, flag_suffix


def _node_as_tensor(node: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    node_tensor = {}
    _len_suffix = len(_SUFFIX)
    for key, data in node.items():
        if key[-_len_suffix:] == _SUFFIX:
            node_tensor[key] = data
        else:
            node_tensor[key + _SUFFIX] = data

    return node_tensor


class TpuRunner:
    """Runner for IVA TPU."""

    def __init__(self, program_path: str, device_name: str = None, loop: Any = None, sync: bool = False, pyprocessing: bool = False) -> None:

        LOGGER.debug(f'Init TpuRunner with program: {program_path}')

        self._pyprocessing = pyprocessing
        self._sync = sync
        self._loop = loop if loop else asyncio.get_event_loop()

        tpu_devices = get_tpu_devices()
        if len(tpu_devices) < 1:
            raise EnvironmentError('No TPU devices found')
        
        # import ipdb; ipdb.set_trace()
        if device_name is None:
        # device_num = int(list(filter(str.isdigit, tpu_devices[0]))[0])
            self._device = TPUDevice(tpu_devices[0].encode('utf-8'))
        else:
            full_name = [name for name in tpu_devices if device_name in name]
            assert len(full_name) == 1, f'More than one device selected: {full_name}'
            assert full_name[0] in tpu_devices, f'No such device: {device_name}'
            self._device = TPUDevice(full_name[0].encode('utf-8'))
        
        if self._device.init() != 0:
            print('\n\nDevice error: {}\n'.format(self._device.get_error().decode('utf-8')))

        if pyprocessing:
            with tempfile.TemporaryDirectory() as tempdir:
                with ZipFile(program_path, 'r') as zip_obj:
                    zip_obj.extractall(tempdir)

                with open(os.path.join(tempdir, 'metadata.json'), 'r') as metadata_file:
                    metadata = json.load(metadata_file)

                tpu_par = get_tpu_parameters(metadata['hardware_parameters'])

                tensor_descriptions: Dict[str, TensorDescription] = dict()
                for _, region in metadata['inputs'].items():
                    for name, io_ in region.items():
                        tensor_descriptions[name] = _get_tensor_description(io_, tpu_par.cache_word_length)
                        LOGGER.debug(f'Input: {name}, {[len(s) for s in tensor_descriptions[name].user_shape_mask]}, '
                                     f'{tensor_descriptions[name].user_dtype}')

                for _, region in metadata['outputs'].items():
                    for name, io_ in region.items():
                        tensor_descriptions[name] = _get_tensor_description(io_, tpu_par.cache_word_length)

                with open(os.path.join(tempdir, 'metadata.json'), 'w') as metadata_file:
                    raw_metadata = to_raw(metadata)
                    json.dump(raw_metadata, metadata_file)

                with tempfile.NamedTemporaryFile() as temp_file:
                    program_path = os.path.join(tempdir, 'program_raw.tpu')
                    shutil.make_archive(temp_file.name, 'zip', tempdir)
                    os.rename(temp_file.name + '.zip', program_path)
                    LOGGER.debug(f'Raw program saved to {program_path}')

                self._tpu_par = tpu_par
                self._tensor_descriptions = tensor_descriptions
        
        self._program = TPUProgram(program_path.encode('utf-8'))
        self._device.load_program(self._program)

        if not bool(self._program.is_valid()):
            print('\n\nProgram Error: {}\n'.format(self._program.get_error().decode('utf-8')))

    def __call__(self, input_data: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """
        Run inference using IVA TPU.

        Parameters
        ----------
        input_data
            Dict with input tensors for inference

        """

        input_data, flag_suffix = _tensor_as_node(input_data)
        
        if self._pyprocessing:
            mode = TPUProcessingMode.kRaw.value
            input_data = pre_process(self._tpu_par, input_data, self._tensor_descriptions)
            # Convert to raw program format
            input_data = {n: v.reshape((1, -1)).view(np.int8) for n, v in input_data.items()}
        else:
            mode = TPUProcessingMode.kFull.value

        inference = TPUInference(self._program)
        tpu_input_buf, tpu_output_buf, ctx = load_inference(input_data, self._program)
        
        inference.set_inputs(tpu_input_buf)
        inference.set_outputs(tpu_output_buf)

        if self._sync:
            self._device.run_inference(inference, mode)
        else:
            status_future = submit_inference(self._device, self._program, inference, tpu_output_buf, mode)
            self._loop.run_until_complete(status_future)
        output_data = get_inference(self._program, tpu_output_buf, ctx, as_dict=True)
        if self._pyprocessing:
            output_data = post_process(self._tpu_par, output_data, self._tensor_descriptions)
        if flag_suffix:
            output_data = _node_as_tensor(output_data)

        return output_data
