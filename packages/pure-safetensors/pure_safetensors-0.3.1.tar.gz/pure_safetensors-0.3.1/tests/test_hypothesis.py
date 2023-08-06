import pytest

import numpy
import pure_safetensors

from .conftest import RUN_SLOW_TESTS, SPARSE, temporary_dir

try:
    import hypothesis
    from hypothesis import strategies as st
except ImportError:
    pytest.skip("hypothesis not installed, skipping", allow_module_level=True)


sizes_strategy = st.sampled_from((0, 1, 8, 4095, 8193))


@hypothesis.given(
    tensor_writes=st.lists(st.tuples(st.integers(1, 4), sizes_strategy), max_size=10),
    use_mmap=st.booleans(),
)
@hypothesis.settings(max_examples=10000 if RUN_SLOW_TESTS else 200, deadline=None)
def test_hypothesis(tensor_writes, use_mmap):
    settings = pure_safetensors.Settings()
    settings.header_size_alignment = 1
    settings.header_size_padding = 0

    correct_tensors = {}

    rand = numpy.random.RandomState(420)

    kw = dict(settings=settings, sparse=True if SPARSE else None)

    with temporary_dir() as tmp:
        path = tmp / "x.safetensors"
        path.write_bytes(b"")

        for step, (index, size) in enumerate(tensor_writes):
            with pure_safetensors.SafeTensors(path, mode="r+", **kw) as sf:
                adapter = sf.as_numpy()
                tensor = rand.randint(0, 255, dtype="uint8", size=(size,))

                # we might need to delete an older tensor
                if index in correct_tensors:
                    old_name, old_tensor = correct_tensors[index]

                    # check that the data in it is fine first
                    assert adapter[old_name].tobytes() == old_tensor.tobytes()

                    # then delete it!
                    del adapter[old_name]

                name = "tensor" + ("x" * (step * 100))

                # write the new tensor
                adapter[name] = tensor
                correct_tensors[index] = (name, tensor)

            with pure_safetensors.SafeTensors(path, mode="c", **kw) as sf:
                adapter = sf.as_numpy()
                for k, (name, tensor) in correct_tensors.items():
                    assert adapter[name].tobytes() == tensor.tobytes()
                    sf.flush(free=True)  # free up memory!
