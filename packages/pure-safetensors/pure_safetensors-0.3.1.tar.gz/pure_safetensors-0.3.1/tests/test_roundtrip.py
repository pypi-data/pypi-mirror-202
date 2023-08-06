import pytest
import numpy as np
from collections import OrderedDict

import pure_safetensors
from .conftest import temporary_dir


def _roundtrip(tensors, tight, use_mmap):
    settings = pure_safetensors.Settings()
    if tight:
        settings.header_size_alignment = 1
        settings.header_size_padding = 0

    tensors = OrderedDict(tensors)
    with temporary_dir() as tmp:
        path = tmp / "file.safetensors"
        kw = dict(settings=settings, use_mmap=use_mmap)

        with pure_safetensors.SafeTensors(path, mode="w+", **kw) as sf:
            m = sf.as_numpy()
            m.update(tensors)
            orig_dtype_shape = {
                k: (info.dtype, info.shape) for k, info in sf.tensors.items()
            }

        with pure_safetensors.SafeTensors(path, mode="r+", **kw) as sf:
            m = sf.as_numpy()
            for k, v in tensors.items():
                assert m[k].tobytes() == v.tobytes()
                assert m[k].dtype == v.dtype

        with pure_safetensors.SafeTensors(path, mode="r+", **kw) as sf:
            m = sf.as_buffer()
            for k, v in tensors.items():
                buf, dt, shape = m[k]
                assert buf == v.tobytes()
                o_dt, o_shape = orig_dtype_shape[k]
                assert o_dt.name == dt.name
                assert o_shape == shape


@pytest.mark.parametrize("use_mmap", (False, True))
@pytest.mark.parametrize("tight", (False, True))
@pytest.mark.parametrize("dtype", pure_safetensors.dtypes.keys())
@pytest.mark.parametrize(
    "shape", [(), (0,), (3,), (3, 4), (3, 4, 5), (2, 3, 4, 5), (4, 7, 0, 3)]
)
def test_roundtrip_numpy_single(use_mmap, tight, dtype, shape):
    dtype = pure_safetensors.dtypes[dtype]
    if shape:
        mg = np.meshgrid(*(range(size) for size in shape))
        tensor = sum(a * i for i, a in enumerate(mg, 1))
    else:
        tensor = np.zeros(shape=shape)

    if dtype.name == "BF16":
        pytest.skip("bfloat16 not supported in numpy")

    tensor = tensor.astype(dtype.numpy_name, order="C", casting="unsafe")

    _roundtrip({"name": tensor}, tight=tight, use_mmap=use_mmap)
