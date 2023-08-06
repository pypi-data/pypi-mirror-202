from typing import Tuple

import attr
import numpy

from .safetensors import dtypes, DType, SafeTensorInfo
from .adapter import BaseAdapter, _Buffer


@attr.s(eq=False)
class NumpyAdapter(BaseAdapter):
    bfloat16_as_uint16: bool = attr.ib(default=False)

    NUMPY_DTYPES_MAP = {dt.numpy_name: dt for dt in dtypes.values()}

    def map_tensor_dtype_to_numpy(self, dtype: DType):
        dtype_name = dtype.numpy_name

        if dtype_name == "bfloat16" and self.bfloat16_as_uint16:
            dtype_name = "u2"

        return numpy.dtype(dtype_name).newbyteorder("<")

    def _user_data_to_safetensor_info(self, array):
        if type(array) is tuple:
            array, dtype = array
        else:
            dtype = None

        if dtype is None:
            dtype = self.NUMPY_DTYPES_MAP[array.dtype.name]

        return SafeTensorInfo(dtype=dtype, start=0, end=0, shape=array.shape)

    def _copy_user_data_into_existing_tensor(self, data: object, key: str):
        self[key][...] = data

    def _memory_buffer_as_numpy_array(
        self, tensor: SafeTensorInfo, buffer: _Buffer
    ) -> Tuple[numpy.ndarray]:
        dtype = self.map_tensor_dtype_to_numpy(tensor.dtype)
        shape = tensor.shape

        return numpy.frombuffer(buffer, dtype=dtype).reshape(shape)

    def __getitem__(self, key):
        tensor, mem_mapping = self.s.get_memory_mapping_for_tensor(key)
        return self._memory_buffer_as_numpy_array(tensor, mem_mapping.buffer)
