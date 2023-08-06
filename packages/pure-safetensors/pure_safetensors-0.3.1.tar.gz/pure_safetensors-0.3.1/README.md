# pure_safetensors

[Safetensors](https://github.com/huggingface/safetensors) library but in pure clean Python. Run it on PyPy or IronPython or wherever.

# Dependencies

We try to keep dependencies light:

- [attrs](https://pypi.org/project/attrs/) dataclass library (2881 LoC)
- [marshmallow](https://pypi.org/project/marshmallow/) serialization and validation library (2647 LoC)
- [sortedcollections](https://pypi.org/project/sortedcollections/) tiny sorted collections library (339 LoC) built on top of [sortedcontainers](https://pypi.org/project/sortedcontainers/) (1493 LoC)
- (optional) [sparsefile](https://pypi.org/project/sparsefile/) sparse file library (191 LoC)
- (optional) [fickle](https://pypi.org/project/fickle/) whitelist-based firewall for safe pickle loading, used for PyTorch model conversion (926 LoC)

Optionally, this library integrates with NumPy (if available). PyTorch integration is planned, someday.

To run the tests, you'll need `pytest`, `numpy`, and optionally `hypothesis`.

# Examples

```python
from pure_safetensors import SafeTensors

with SafeTensors("/path/to/example.safetensors", "r+") as sf:
    arrays = sf.as_numpy()
    arrays["hello"][3, :] += 420.69
    arrays["world"] = arrays["hello"][0:2] * 10

    # assign multiple arrays! much faster!
    arrays.update(
        {
            "q": my_array_1,
            "k": my_array_2,
            "v": my_array_3,
        }
    )

    # delete arrays! such wonders!
    del arrays["v"]
```

Do you have an existing PyTorch checkpoint model that you would like to safetensors? Then try running:

```sh
python3 -m pure_safetensors import-pytorch /path/to/model.ckpt /path/to/model.safetensors
```

# Bugs

The space allocator is a greedy algorithm based on first-fit-decreasing bin packing. So if you add/remove tensors to an existing file, it may leave too much empty space behind.

PyTorch support isn't implemented yet.

# Alternatives

- [safetensors](https://github.com/huggingface/safetensors/)
- [Narsil/pure_torch.py](https://gist.github.com/Narsil/3edeec2669a5e94e4707aa0f901d2282)
- [Narsil/safetensors.cpp](https://gist.github.com/Narsil/5d6bf307995158ad2c4994f323967284)

|                                                 | pure_safetensors | safetensors | pure_torch.py | safetensors.cpp |
|-------------------------------------------------|------------------|-------------|---------------|-----------------|
| Written in pure Python?                         | ✅ | ❌ | ✅ | — |
| Supports NumPy (without PyTorch)?               | ✅ | ✅ | ❌ | — |
| Supports PyTorch?                               | ❌ | ✅ | ✅ | — |
| Can work without numpy or pytorch?              | ✅ | ✅ | ❌ | — |
| Can write safetensors files?                    | ✅ | ✅ | ❌ | ❌ |
| Can modify file in-place to add/remove tensors? | ✅ | ❌ | ❌ | ❌ |
| Has test suite?                                 | ✅ | ✅ | ❌ | ❌ |
| Stable API?                                     | 🤷 | ✅ | ❔ | ❔ |
| Automatically makes files sparse to save space? | ✅ | ❌ | ❌ | ❌ |
| Works on platforms without mmap?                | ✅ | ❌ | ❌ | ❌ |
