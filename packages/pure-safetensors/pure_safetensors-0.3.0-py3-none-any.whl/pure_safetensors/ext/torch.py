from pathlib import Path
from typing import Dict, Tuple
import zipfile

import attr
from fickle import Unknown, UnknownImport
from fickle.ext.pytorch import fake_torch_load_zipped, StoredTensor
from pure_safetensors import DType, SafeTensors
from pure_safetensors.numpy import NumpyAdapter
import tqdm

import json


@attr.s(eq=False)
class _TensorConversionInfo:
    stored_tensor: StoredTensor = attr.ib()
    dtype: DType = attr.ib()
    shape: Tuple[int] = attr.ib()


@attr.s(eq=False)
class PyTorchSafetensorsConverter:
    safe_tensors: SafeTensors = attr.ib()
    torch_checkpoint: dict = attr.ib()

    def _sanitize_json(self, obj):
        if isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        elif isinstance(obj, (tuple, list)):
            return tuple(self._sanitize_json(x) for x in obj)
        elif isinstance(obj, dict):
            return {
                str(self._sanitize_json(k)): self._sanitize_json(v)
                for k, v in obj.items()
            }
        elif isinstance(obj, UnknownImport):
            return str(obj)
        elif isinstance(obj, Unknown):
            return self._sanitize_json(attr.asdict(obj, recurse=False))

        return repr(obj)

    def convert_metadata(self, metadata: dict):
        return {
            key: json.dumps(self._sanitize_json(value))
            for key, value in metadata.items()
        }

    def convert_and_store_tensor(self, key: str, info: _TensorConversionInfo):
        m = self.safe_tensors.as_buffer()
        m[key][0][:] = info.stored_tensor.buffer

    def get_tensor_conversion_info(self, key: str, stored_tensor: StoredTensor):
        dtype = NumpyAdapter.NUMPY_DTYPES_MAP[stored_tensor.storage.dtype]
        return key, _TensorConversionInfo(
            stored_tensor=stored_tensor, dtype=dtype, shape=stored_tensor.size
        )

    def run(self):
        d = self.torch_checkpoint.copy()
        state_dict = d.pop("state_dict")
        self.safe_tensors.metadata = self.convert_metadata(d)
        tensor_conversion_info: Dict[str, _TensorConversionInfo] = dict(
            self.get_tensor_conversion_info(key, stored_tensor)
            for key, stored_tensor in state_dict.items()
        )

        # allocate space
        self.safe_tensors.as_buffer().update(
            (key, (None, info.dtype, info.shape))
            for key, info in tensor_conversion_info.items()
        )

        total_bytes = sum(
            inf.stored_tensor.size_in_bytes for inf in tensor_conversion_info.values()
        )
        with tqdm.tqdm(
            total=total_bytes, unit="B", unit_scale=True, unit_divisor=1024
        ) as pbar:
            for key, info in tensor_conversion_info.items():
                self.convert_and_store_tensor(key, info)
                self.safe_tensors.flush(free=True)
                pbar.update(info.stored_tensor.size_in_bytes)

    @classmethod
    def convert(cls, torch_checkpoint: Path, safe_tensors: Path):
        with open(torch_checkpoint, "rb") as f_src, zipfile.ZipFile(
            f_src
        ) as zf, SafeTensors(safe_tensors, "x+") as st:
            torch_checkpoint_dict = fake_torch_load_zipped(zf)
            instance = cls(safe_tensors=st, torch_checkpoint=torch_checkpoint_dict)
            instance.run()
