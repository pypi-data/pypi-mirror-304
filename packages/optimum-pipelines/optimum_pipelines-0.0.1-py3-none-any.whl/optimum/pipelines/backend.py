# Copyright 2024 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
import sys
import warnings
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from optimum.pipelines import is_torch_available, is_transformers_available


if is_torch_available():
    import torch


class Backend(ABC):
    @abstractmethod
    def get_default_model_for_task(self, task: str) -> str:
        """Get the default model for the specified task

        If the caller did not specify a pretrained model or path when calling the pipeline()
        factory method, the backend will provide a default model for the specified task.

        Returns:
            A string, the `model id` of a pretrained model hosted inside a model repo on huggingface.co.
        """
        raise NotImplementedError

    @abstractmethod
    def get_pipeline_for_task(
        self, task: str, pretrained_model_name_or_path: Union[str, Path], *, token: Optional[Union[str, bool]] = None
    ):
        """Dispatch method to be implemented by each backend

        This dispatch method must return the Pipeline class for the specified task.

        It takes an optional parameter corresponding to the model in order to allow the
        backend to support specialized pipeline classes for specific model architectures.
        For instance, the backend could return two different pipeline classes for 'text-generation':
        one for encoder-decoder models, and the other for decoder models.

        Args:
            task (`str`): the task to provide a `Pipeline` class for.
            pretrained_model_name_or_path (`Union[str,os.PathLike]`):
                Can be either:
                    - A string, the `model id` of a pretrained model hosted inside a
                    model repo on huggingface.co. Valid model ids can be located
                    at the root-level, like `bert-base-uncased`, or namespaced
                    under a user or organization name, like
                    `dbmdz/bert-base-german-cased`.
                    - You can add `revision` by appending `@` at the end of model_id
                    simply like this: `dbmdz/bert-base-german-cased@main` Revision
                    is the specific model version to use. It can be a branch name,
                    a tag name, or a commit id, since we use a git-based system
                    for storing models and other artifacts on huggingface.co, so
                    `revision` can be any identifier allowed by git.
                    - A path to a `directory` containing model weights saved using
                    [`~transformers.PreTrainedModel.save_pretrained`], e.g.,
                    `./my_model_directory/`.
            token (`Optional[str,bool]`):
                The token to use as HTTP bearer authorization for remote files. If
                `True`, will use the token generated when running `transformers-cli
                login` (stored in `~/.huggingface`).
        Returns:
            The corresponding `Pipeline` class.
        """
        raise NotImplementedError

    @abstractmethod
    def get_model_for_task(
        self,
        task: str,
        pretrained_model_name_or_path: Union[str, Path],
        *,
        token: Optional[Union[str, bool]] = None,
        trust_remote_code: Optional[bool] = False,
        dtype: Optional[Union[str, "torch.dtype"]] = "auto",
        device: Optional[Union[int, str, "torch.device"]] = None,
    ) -> Any:
        """Instantiate the model for the specified task

        This instantiates the backend-specific model object for the specified task.

        Args:
            task (`str`): the task for which the model should be instantiated.
            pretrained_model_name_or_path (`Union[str, Path]`):
                Can be either:
                    - A string, the `model id` of a pretrained model hosted inside a
                    model repo on huggingface.co. Valid model ids can be located
                    at the root-level, like `bert-base-uncased`, or namespaced
                    under a user or organization name, like
                    `dbmdz/bert-base-german-cased`.
                    - You can add `revision` by appending `@` at the end of model_id
                    simply like this: `dbmdz/bert-base-german-cased@main` Revision
                    is the specific model version to use. It can be a branch name,
                    a tag name, or a commit id, since we use a git-based system
                    for storing models and other artifacts on huggingface.co, so
                    `revision` can be any identifier allowed by git.
                    - A path to a `directory` containing model weights saved using
                    [`~transformers.PreTrainedModel.save_pretrained`], e.g.,
                    `./my_model_directory/`.
            token (`Optional[str, bool]`):
                The token to use as HTTP bearer authorization for remote files. If
                `True`, will use the token generated when running `transformers-cli
                login` (stored in `~/.huggingface`).
            trust_remote_code (`bool`, *optional*, defaults to `False`):
                Whether or not to allow for custom modeling code defined on the Hub. This option
                should only be set to `True` for repositories you trust and in which you have read
                the code, as it will execute code present on the Hub on your local machine.
            dtype (`Optional[Union[str, torch.dtype]]`):
                The precision for this model (`torch.float16`, `torch.bfloat16`, ... or `"auto"`).
            device (`Optional[Union[int, str, torch.device]]`):
                Defines the device (*e.g.*, `"cpu"`, `"cuda:1"`, `"mps"`, or a GPU ordinal rank like `1`) on which this
                pipeline will be allocated.
        Returns:
            The corresponding backend-specific model instance.
        """
        raise NotImplementedError

    @abstractmethod
    def get_pipeline_init_kwargs(
        self,
        task: str,
        pretrained_model_name_or_path: Union[str, Path],
        model: Any,
        *,
        token: Optional[Union[str, bool]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Return the pipeline named initialization parameters

        The pipeline class returned by get_pipeline_for_task will always be instantiated with
        a single positional model parameter.
        In this method, the backend can process the other named parameters that were passed to
        the factory method to define additional named parameters that must be passed to the
        pipeline constructor.
        This typically includes a `Tokenizer` for most NLP tasks.

        Args:
            task (`str`): the task for which the pipeline should be instantiated.
            pretrained_model_name_or_path (`Union[str, Path]`):
                Can be either:
                    - A string, the `model id` of a pretrained model hosted inside a
                    model repo on huggingface.co. Valid model ids can be located
                    at the root-level, like `bert-base-uncased`, or namespaced
                    under a user or organization name, like
                    `dbmdz/bert-base-german-cased`.
                    - You can add `revision` by appending `@` at the end of model_id
                    simply like this: `dbmdz/bert-base-german-cased@main` Revision
                    is the specific model version to use. It can be a branch name,
                    a tag name, or a commit id, since we use a git-based system
                    for storing models and other artifacts on huggingface.co, so
                    `revision` can be any identifier allowed by git.
                    - A path to a `directory` containing model weights saved using
                    [`~transformers.PreTrainedModel.save_pretrained`], e.g.,
                    `./my_model_directory/`.
            model (`Any`): the model instance to be used by the pipeline.
            token (`Optional[str, bool]`):
                The token to use as HTTP bearer authorization for remote files. If
                `True`, will use the token generated when running `transformers-cli
                login` (stored in `~/.huggingface`).
        Returns:
            A dictionary of kwargs.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def tasks(self) -> List[str]:
        """Get the tasks supported by this backend

        Returns:
        A `List[str]` of supported tasks.
        """
        raise NotImplementedError


_BACKENDS = {}


@functools.lru_cache(None)
def _discover_backends():
    """Discover and load external backends

    This discovers the optimum.pipelines.backends entry_points declared in
    external packages installed on the system, and calls them to allow these
    packages to register one or several backends.


    Please refer to https://setuptools.pypa.io/en/latest/userguide/entry_point.html#entry-points-for-plugins
    to see how entry_points should be declared in pyproject.toml or setup.py.
    """
    # Deferred import to load the mocked method in unit tests
    from importlib.metadata import entry_points  # noqa E402

    group_name = "optimum.pipelines.backends"
    if sys.version_info < (3, 10):
        eps = entry_points()
        eps = eps[group_name] if group_name in eps else []
        eps = {ep.name: ep for ep in eps}
    else:
        eps = entry_points(group=group_name)
        eps = {name: eps[name] for name in eps.names}
    for backend_name in eps:
        try:
            # This imports the entry_point function
            ep = eps[backend_name].load()
            # Call the entry_point to allow it to register its backend(s)
            ep()
        except Exception as e:
            warnings.warn(f"An exception occured while loading backend {backend_name}: {e}")


def register_backend(name: str, backend: Backend):
    if name in _BACKENDS:
        warnings.warn(f"Ignoring new backend {name} as another backend is already registered with the same name.")
    if not isinstance(backend, Backend):
        warnings.warn(f"Ignoring {name} backend as it is not an instance of optimum.pipelines.Backend.")
    _BACKENDS[name] = backend


if is_transformers_available():
    # This is temporary: eventually this backend will be registered dynamically
    from .backends.transformers import TransformersBackend  # noqa E402

    register_backend("transformers", TransformersBackend())


def get_backend(backend: str):
    if backend not in _BACKENDS:
        # Look for backends provided by other packages
        _discover_backends()
    if backend not in _BACKENDS:
        raise ValueError(f"Backend '{backend}' not found: did you install the corresponding libraries ?")
    return _BACKENDS[backend]
