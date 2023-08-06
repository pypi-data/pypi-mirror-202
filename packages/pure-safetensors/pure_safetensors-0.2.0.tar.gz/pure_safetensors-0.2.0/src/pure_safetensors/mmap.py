from collections.abc import Mapping, MutableMapping
from typing import Dict, IO, Iterable, NewType, Tuple

import attr

from .util import align, align_down, get_file_size
from .safetensors import DType, SafeTensors, SafeTensorInfo

try:
    import mmap
except ImportError:
    mmap = None


# you can use this global variable to control whether the OS mmap is used
use_mmap = mmap is not None

_Buffer = NewType("_Buffer", object)


@attr.s(eq=False)
class MemoryMapping:
    """
    Thin abstraction around :func:`mmap.mmap`, except the offset and length
    do not have to be multiples of the page size.

    Parameters
    ----------
    file: IO
        File object.
    offset: int
        Offset into the file in bytes. Does not need to be a multiple of page size.
    length: int
        Length of the memory map. Does not need to be a multiple of page size.
    mode: str
        Must be "r", "r+"/"w+", or "c".
    """

    file: IO = attr.ib()
    offset: int = attr.ib()
    length: int = attr.ib()
    mode: str = attr.ib()

    buffer: _Buffer

    def __attrs_post_init__(self):
        self._map()

    def _map(self):
        raise NotImplementedError

    def flush(self):
        raise NotImplementedError


@attr.s(eq=False)
class FakeMemoryMapping(MemoryMapping):
    """
    This is a fake memory mapping which just reads the file data
    into a bytearray and returns it to the user. When the context
    manager (ie "with:" block) is closed, the file data is written
    back if necessary.
    """

    def _map(self):
        b = bytearray(self.length)
        self.file.seek(self.offset)
        if self.file.readinto(b) != self.length:
            raise ValueError("short read")
        self.buffer = b
        return self.buffer

    def flush(self):
        if self.mode != "r" and self.mode != "c":
            self.file.seek(self.offset)
            if self.file.write(self.buffer) != self.length:
                raise ValueError("short write")


@attr.s(eq=False)
class RealMemoryMapping(MemoryMapping):
    def _mmap(self, *, offset, length, **kw):
        f = self.file
        f.flush()

        if get_file_size(f) < length + offset:
            # map the rest of the file if the end of the memory map extends past the end
            # of the file
            length = 0

        return mmap.mmap(f.fileno(), offset=offset, length=length, **kw)

    def _real_mmap_access_kwargs(self) -> int:
        mode = self.mode
        if mode == "c":
            return dict(access=mmap.ACCESS_COPY)
        elif mode == "r":
            return dict(access=mmap.ACCESS_READ)
        else:
            return dict(access=mmap.ACCESS_WRITE)

    def _map(self):
        """
        Map the data into virtual memory.
        """
        kw = self._real_mmap_access_kwargs()

        page_size = mmap.ALLOCATIONGRANULARITY
        offset = align_down(page_size, self.offset)
        end = align(page_size, self.offset + self.length)
        length = end - offset

        if not length:
            # special case for zero-length tensors; note that passing length=0 to mmap
            # causes it to map the entire file
            self.mem = None
            self.buffer = memoryview(bytearray(0))
            return

        mem_offset = self.offset - offset
        self.mem = mem = self._mmap(offset=offset, length=length, **kw)
        self.buffer = memoryview(mem)[mem_offset : mem_offset + self.length]

    def flush(self):
        if self.mem is not None:
            self.mem.flush()


@attr.s(eq=False)
class BaseAdapter(MutableMapping):
    s: SafeTensors = attr.ib()
    use_mmap: bool = attr.ib(factory=lambda: use_mmap)
    mappings: Dict[str, MemoryMapping] = attr.ib(init=False, factory=dict)

    def _copy_user_data_into_existing_tensor(self, data: object, key: str) -> None:
        raise NotImplementedError

    def _user_data_to_safetensor_info(self, data: object) -> SafeTensorInfo:
        raise NotImplementedError

    def _open_memory_mapping(self, offset: int, length: int) -> MemoryMapping:
        cls = RealMemoryMapping if self.use_mmap else FakeMemoryMapping
        return cls(file=self.s.file, offset=offset, length=length, mode=self.s.mode)

    def get_memory_mapping_for_tensor(self, key: str) -> MemoryMapping:
        tensor = self.s.tensors[key]
        mapping = self.mappings.get(key, None)
        if mapping is None:
            self.mappings[key] = mapping = self._open_memory_mapping(
                offset=tensor.start, length=tensor.end - tensor.start
            )
        return mapping

    def flush(self, keys=None, free: bool = False):
        """
        Ensure that tensor data is written to disk. If ``free == True``, then
        remove the memory mapping from the cached memory mappings.
        """
        mappings = self.mappings
        keys = tuple(mappings.keys()) if keys is None else keys
        for key in keys:
            mapping = mappings.get(key, None)
            if mapping is not None:
                mapping.flush()
                if free:
                    mappings.pop(key, None)

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
        self.flush(iterable, free=True)

        for k, user_data in iterable.items():
            if user_data is None:
                continue  # deleted array

            self._copy_user_data_into_existing_tensor(user_data, k)

        self.s.file.flush()

    def __iter__(self):
        return iter(self.s.tensors)

    def __len__(self):
        return len(self.s.tensors)

    def __delitem__(self, key: str):
        self.flush((key,), free=True)
        self[key] = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.flush(free=True)


@attr.s(eq=False)
class BufferAdapter(BaseAdapter):
    def _copy_user_data_into_existing_tensor(self, data: object, key: str):
        self[key][:] = data

    def _user_data_to_safetensor_info(self, data):
        array, dtype = data
        return SafeTensorInfo(dtype=dtype, start=0, end=0, shape=array.shape)

    def __getitem__(self, key: str) -> Tuple[_Buffer, DType]:
        return (
            self.get_memory_mapping_for_tensor(key).buffer,
            self.s.tensors[key].dtype,
        )

    def __setitem__(self, key: str, value: Tuple[_Buffer, DType]):
        self.update(((key, value),))
