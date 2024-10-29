import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from unittest.mock import MagicMock, patch

import pytest

from optimum.pipelines import is_transformers_available, pipeline
from optimum.pipelines.backend import Backend, get_backend, register_backend


TEXT_GENERATION_OUTPUT = (
    "If it looks like a duck, swims like a duck, and quacks like a duck, then it probably is a duck."
)
TRANSLATION_OUTPUT = (
    "Les boutiques de fleuristes n'ont jamais de rideau de fer. Personne ne cherche à voler des fleurs."
)


@dataclass
class CustomModel:
    task: str
    pretrained_model_name_or_path: Union[str, Path]
    token: Optional[Union[str, bool]] = None
    trust_remote_code: Optional[bool] = False
    dtype: Optional[Any] = None
    device: Optional[Any] = None


@dataclass
class CustomPipeline:
    model: CustomModel
    hard_coded_output: str

    def __call__(self, input: str):
        return self.hard_coded_output


class CustomTextGenerationPipeline(CustomPipeline):
    pass


class CustomTranslationPipeline(CustomPipeline):
    pass


_CUSTOM_TASKS = {
    "text-generation": {
        "default_model": "foo/bar",
        "pipeline_cls": CustomTranslationPipeline,
    },
    "translation": {
        "default_model": "baz/qux",
        "pipeline_cls": CustomTranslationPipeline,
    },
}


class CustomBackend(Backend):
    def get_default_model_for_task(self, task: str) -> str:
        return _CUSTOM_TASKS[task]["default_model"]

    def get_pipeline_for_task(self, task: str):
        return _CUSTOM_TASKS[task]["pipeline_cls"]

    def get_model_for_task(
        self,
        task: str,
        pretrained_model_name_or_path: Union[str, Path],
        *,
        token: Optional[Union[str, bool]] = None,
        trust_remote_code: Optional[bool] = False,
        dtype: Optional[str] = "auto",
        device: Optional[Union[int, str]] = None,
    ) -> Any:
        return CustomModel(
            task=task,
            pretrained_model_name_or_path=pretrained_model_name_or_path,
            token=token,
            trust_remote_code=trust_remote_code,
            dtype=dtype,
            device=device,
        )

    def get_pipeline_init_kwargs(
        self,
        task: str,
        pretrained_model_name_or_path: Union[str, Path],
        model: Any,
        *,
        token: Optional[Union[str, bool]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        hard_coded_output = TEXT_GENERATION_OUTPUT if task == "text-generation" else TRANSLATION_OUTPUT
        return {"hard_coded_output": hard_coded_output}

    @property
    def tasks(self) -> List[str]:
        return _CUSTOM_TASKS.keys()


def custom_entry_point():
    """In an external package, this method would be declared as the
    backend entry_point directly in the setup.py or pyproject.toml.
    Here we mock the importlib.metadata entry_points method to return it.
    """
    register_backend("custom", CustomBackend())


ep_name = "custom_entry_point_name"
mock_3_9 = MagicMock()
mock_3_9.load.return_value = custom_entry_point
mock_3_9.name = ep_name

mock_3_10 = MagicMock()
mock_3_10.load.return_value = custom_entry_point

backends_group = "optimum.pipelines.backends"


def mock_entry_points(group=None):
    if sys.version_info < (3, 10):
        return {backends_group: [mock_3_9]}
    else:
        assert group == backends_group, group
        mock_group = MagicMock()
        mock_group.names = [ep_name]
        mock_group.__getitem__ = lambda self, key: mock_3_10
        return mock_group


def test_custom_backend_get_backend():
    with patch("importlib.metadata.entry_points", mock_entry_points):
        backend = get_backend("custom")
        assert isinstance(backend, CustomBackend)


@pytest.mark.skipif(not is_transformers_available(), reason="transformers is not available")
def test_custom_backend_get_transformers_backend():
    with patch("importlib.metadata.entry_points", mock_entry_points):
        backend = get_backend("transformers")
        assert isinstance(backend, Backend)


@pytest.mark.parametrize("task", _CUSTOM_TASKS.keys())
def test_custom_backend_pipeline_default_model(task):
    with patch("importlib.metadata.entry_points", mock_entry_points):
        pipe = pipeline(task, backend="custom")
        expected_cls = _CUSTOM_TASKS[task]["pipeline_cls"]
        assert type(pipe) is expected_cls
        assert type(pipe.model) is CustomModel
        expected_output = TEXT_GENERATION_OUTPUT if task == "text-generation" else TRANSLATION_OUTPUT
        assert pipe("My name is David and I") == expected_output
