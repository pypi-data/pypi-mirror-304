import importlib

import pytest

from optimum.pipelines.generated import tasks


@pytest.fixture(scope="package", params=tasks)
def task(request):
    return request.param


if importlib.util.find_spec("torch") is not None:
    import torch

    devices = ["cpu"]
    if torch.cuda.is_available():
        devices += ["cuda"]
    elif torch.backends.mps.is_available():
        devices += ["mps"]

    @pytest.fixture(scope="module", params=devices)
    def device(request):
        return torch.device(request.param)
