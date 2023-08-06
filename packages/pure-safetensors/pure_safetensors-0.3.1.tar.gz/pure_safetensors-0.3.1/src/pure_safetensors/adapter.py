from collections.abc import Mapping, MutableMapping
from typing import Iterable, Optional, Tuple

import attr

from .mmap import _Buffer
from .safetensors import DType, SafeTensors, SafeTensorInfo


@attr.s(eq=False)
class BaseAdapter(MutableMapping):
    s: SafeTensors = attr.ib()

    def _copy_user_data_into_existing_tensor(self, data: object, key: str) -> None:
        raise NotImplementedError

    def _user_data_to_safetensor_info(self, data: object) -> SafeTensorInfo:
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def __setitem__(self, key, value):
        self.update(((key, value),))

    def update(self, iterable: Iterable[Tuple[str, object]]):
        if not isinstance(iterable, Mapping):
            iterable = dict(iterable)

        f = self._user_data_to_safetensor_info
        safetensor_infos = {
            name: (None if x is None else f(x)) for name, x in iterable.items()
        }

        # allocate/deallocate tensors
        self.s.create_or_replace_or_delete_tensors(safetensor_infos)

        # flush existing memory maps
        self.s.flush(iterable, free=True)

        for k, user_data in iterable.items():
            if user_data is None:
                continue  # deleted array

            self._copy_user_data_into_existing_tensor(user_data, k)

        self.s.flush(iterable)

    def __iter__(self):
        return iter(self.s.tensors)

    def __len__(self):
        return len(self.s.tensors)

    def __delitem__(self, key: str):
        self.s.flush((key,), free=True)
        self[key] = None


@attr.s(eq=False)
class BufferAdapter(BaseAdapter):
    def _copy_user_data_into_existing_tensor(self, data: object, key: str):
        array, dtype, shape = data
        if array is not None:
            self[key][0][:] = array

    def _user_data_to_safetensor_info(self, data):
        array, dtype, shape = data
        return SafeTensorInfo(dtype=dtype, start=0, end=0, shape=shape)

    def __getitem__(self, key: str) -> Tuple[_Buffer, DType, Tuple[int]]:
        info, mem_mapping = self.s.get_memory_mapping_for_tensor(key)
        return (mem_mapping.buffer, info.dtype, info.shape)

    def __setitem__(self, key: str, value: Tuple[Optional[_Buffer], DType, Tuple[int]]):
        self.update(((key, value),))
