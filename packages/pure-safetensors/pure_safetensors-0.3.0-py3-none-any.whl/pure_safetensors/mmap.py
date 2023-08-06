from typing import IO, NewType

import attr

from .util import align, align_down, get_file_size

try:
    import mmap
except ImportError:
    mmap = None

_Buffer = NewType("_Buffer", object)


@attr.s(eq=False)
class MemoryMappingFactory:
    """
    Thin abstraction around :func:`mmap.mmap`, except the offset and length
    do not have to be multiples of the page size.

    Parameters
    ----------
    file: IO
        File object.
    mode: str
        Must be "r", "r+"/"w+", or "c".
    """

    file: IO = attr.ib()
    mode: str = attr.ib()

    def map(self, offset: int, length: int) -> "MemoryMapping":
        raise NotImplementedError


@attr.s(eq=False)
class FakeMemoryMappingFactory(MemoryMappingFactory):
    def map(self, offset: int, length: int):
        return FakeMemoryMapping(factory=self, offset=offset, length=length)


@attr.s(eq=False)
class RealMemoryMappingFactory(MemoryMappingFactory):
    """
    Memory mapping backed by actual OS support.
    """

    def __attrs_post_init__(self):
        self._map_full()

    def map(self, offset: int, length: int) -> "MemoryMapping":
        self.remap_if_necessary(offset + length)
        return RealMemoryMapping(factory=self, offset=offset, length=length)

    def remap_if_necessary(self, size):
        """
        Create a new OS mmap if the file grew and the size of the older mmap is smaller
        than ``size``.
        """
        if len(self.memoryview) < size:
            if get_file_size(self.file) < size:
                raise AssertionError(f"file {self.file!r} too short < {size}")
            self._map_full()

    def _map_full(self):
        """
        Map the entire file into virtual memory.
        """
        kw = self._real_mmap_access_kwargs()
        self.file.flush()
        if not get_file_size(self.file):
            self.os_mmap = None
            self.memoryview = memoryview(bytearray(0))
        else:
            self.os_mmap = os_mmap = mmap.mmap(self.file.fileno(), length=0, **kw)
            self.memoryview = memoryview(os_mmap)

    def flush(self):
        m = self.os_mmap
        if m is not None:
            return m.flush()

    def _real_mmap_access_kwargs(self) -> int:
        mode = self.mode
        if mode == "c":
            return dict(access=mmap.ACCESS_COPY)
        elif mode == "r":
            return dict(access=mmap.ACCESS_READ)
        else:
            return dict(access=mmap.ACCESS_WRITE)


@attr.s(eq=False)
class MemoryMapping:
    """
    Parameters
    ----------
    offset: int
        Offset into the file in bytes. Does not need to be a multiple of page size.
    length: int
        Length of the memory map. Does not need to be a multiple of page size.
    """

    factory: MemoryMappingFactory = attr.ib()
    offset: int = attr.ib()
    length: int = attr.ib()

    buffer: _Buffer

    @property
    def file(self):
        return self.factory.file

    @property
    def mode(self):
        return self.factory.mode

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

    def __attrs_post_init__(self):
        self._map()

    def _map(self):
        b = bytearray(self.length)
        self.file.seek(self.offset)
        if self.file.readinto(b) != self.length:
            raise ValueError("short read")
        self.buffer = b
        return b

    def flush(self):
        if self.mode != "r" and self.mode != "c":
            self.file.seek(self.offset)
            if self.file.write(self.buffer) != self.length:
                raise ValueError("short write")


@attr.s(eq=False)
class RealMemoryMapping(MemoryMapping):
    factory: RealMemoryMappingFactory

    @property
    def buffer(self):
        if not self.length:
            return memoryview(bytearray(0))
        else:
            return self.factory.memoryview[self.offset : self.offset + self.length]

    def flush(self):
        self.factory.flush()
