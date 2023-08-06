import argparse
import json
from pathlib import Path

from .safetensors import SafeTensors


class Main:
    def __init__(self, argv):
        self.argument_parser = self.init_argparser()
        self.a = self.argument_parser.parse_args(argv)

    def cmd_missing(self):
        self.argument_parser.error("missing command")

    def cmd_ls(self):
        with SafeTensors(self.a.safetensors, "r") as sf:
            print("metadata:")
            print(json.dumps(sf.metadata, indent=2, sort_keys=True))
            print("tensors:")
            for k in sorted(sf.tensors):
                t = sf.tensors[k]
                print(
                    f"  {t.start:>12d}-{t.end:<12d} "
                    f"{t.shape!r:>20s} {t.dtype.name:4s} {k!r:s}"
                )

    def cmd_pytorch_import(self):
        from .ext.torch import PyTorchSafetensorsConverter

        PyTorchSafetensorsConverter.convert(
            torch_checkpoint=self.a.pytorch_file, safe_tensors=self.a.safetensors
        )

    def init_argparser(self):
        parser = argparse.ArgumentParser()
        parser.set_defaults(callback=self.cmd_missing)
        subparsers = parser.add_subparsers()

        def _Path(x):
            return Path(x).resolve()

        ls = subparsers.add_parser("ls", help="List contents of a safetensors file.")
        ls.add_argument("safetensors", help="Safetensors input file")
        ls.set_defaults(callback=self.cmd_ls)
        # cp = subparsers.add_parser(
        #     "cp",
        #     help="Copy safetensors file, compacting its contents.",
        # )
        # cp.set_defaults(callback=self.cmd_cp)

        pytorch_import = subparsers.add_parser(
            "import-pytorch", help='Import pytorch ".ckpt" file'
        )
        pytorch_import.add_argument(
            "pytorch_file", type=_Path, help="PyTorch .ckpt checkpoint file (source)"
        )
        pytorch_import.add_argument(
            "safetensors", type=_Path, help="Safetensors file (destination)"
        )
        pytorch_import.set_defaults(callback=self.cmd_pytorch_import)

        return parser

    def run(self):
        self.a.callback()

    @classmethod
    def main(cls, argv=None):
        cls(argv=argv).run()


if __name__ == "__main__":
    Main.main()
