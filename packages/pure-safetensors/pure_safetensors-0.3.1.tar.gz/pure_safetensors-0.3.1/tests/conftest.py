import contextlib
import os
import pathlib
import tempfile


RUN_SLOW_TESTS = bool(os.getenv("SLOW", ""))
SPARSE = bool(os.getenv("SPARSE", ""))


@contextlib.contextmanager
def temporary_dir(**kw):
    # use in-RAM filesystem if available
    shm_path = pathlib.Path("/dev/shm")
    if shm_path.is_dir():
        kw.setdefault("dir", str(shm_path))

    with tempfile.TemporaryDirectory(**kw) as dirname:
        yield pathlib.Path(dirname)
