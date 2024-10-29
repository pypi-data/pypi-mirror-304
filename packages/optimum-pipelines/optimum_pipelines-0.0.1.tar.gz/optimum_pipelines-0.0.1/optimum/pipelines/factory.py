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
import warnings
from pathlib import Path
from typing import Optional, Union

from optimum.pipelines.backend import get_backend
from optimum.pipelines.depends import is_torch_available, is_transformers_available


if is_torch_available():
    import torch

if is_transformers_available():
    from transformers import PreTrainedModel


def pipeline(
    task: str,
    *,
    backend: Optional[str] = "transformers",
    model: Optional[Union[str, Path, "PreTrainedModel"]] = None,
    token: Optional[Union[str, bool]] = None,
    trust_remote_code: Optional[bool] = False,
    dtype: Optional[Union[str, "torch.dtype"]] = "auto",
    device: Optional[Union[int, str, "torch.device"]] = None,
    **kwargs,
):
    """Create a pipeline for the specified task

    This method returns the `Pipeline` class for the specified task.

    Args:
        task (`str`): the task to provide a `Pipeline` class for.
        model (`Optional[Union[str, Path, Any]]`):
            The model that will be used by the pipeline to make predictions. This can be a model identifier,
             a path to a local pre-trained model or a backend-specific model instance.
        token (`Optional[str,bool]`):
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
        The corresponding backend-specific pipeline class.
    """
    bk = get_backend(backend)
    if task not in bk.tasks:
        raise ValueError(f"'{task}' is not supported by the '{backend}' backend.")
    if model is None:
        model = bk.get_default_model_for_task(task)
    if isinstance(model, (str, Path)):
        pretrained_model_name_or_path = model
        model = bk.get_model_for_task(
            task,
            pretrained_model_name_or_path,
            token=token,
            trust_remote_code=trust_remote_code,
            dtype=dtype,
            device=device,
        )
        pipeline_kwargs = bk.get_pipeline_init_kwargs(
            task, pretrained_model_name_or_path, model, token=token, **kwargs
        )
    else:
        pipeline_kwargs = kwargs
        if device is not None:
            warnings.warn("Ignoring device parameter as Pipelines cannot change the device of an instantiated model.")
        if dtype != "auto":
            warnings.warn("Ignoring dtype parameter as Pipelines cannot change the device of an instantiated model.")
    cls = bk.get_pipeline_for_task(task)
    return cls(model, **pipeline_kwargs)
