from typing import Tuple

import attr
import numpy

from .safetensors import dtypes, DType, SafeTensorInfo
from .mmap import BaseAdapter, _Buffer


@attr.s(eq=False)
class NumpyAdapter(BaseAdapter):
    bfloat16_as_uint16: bool = attr.ib(default=False)

    numpy_dtypes_map = {dt.numpy_name: dt for dt in dtypes.values()}

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
            dtype = self.numpy_dtypes_map[array.dtype.name]

        return SafeTensorInfo(dtype=dtype, start=0, end=0, shape=array.shape)

    def _copy_user_data_into_existing_tensor(self, data: object, key: str):
        self[key][...] = data

    def memory_buffer_as_numpy_array(
        self, tensor: SafeTensorInfo, buffer: _Buffer
    ) -> Tuple[numpy.ndarray]:
        dtype = self.map_tensor_dtype_to_numpy(tensor.dtype)
        shape = tensor.shape

        cls = numpy.ndarray
        array = cls.__new__(cls, shape=shape, dtype=dtype, buffer=buffer, order="C")

        return array.reshape(shape)

    def __getitem__(self, key):
        tensor = self.s.tensors[key]
        mmapping = self.get_memory_mapping_for_tensor(key)
        return self.memory_buffer_as_numpy_array(tensor, mmapping.buffer)
