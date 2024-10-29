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

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from transformers import (
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    PreTrainedModel,
    is_torch_available,
)
from transformers.models.auto.feature_extraction_auto import FEATURE_EXTRACTOR_MAPPING, AutoFeatureExtractor
from transformers.models.auto.image_processing_auto import IMAGE_PROCESSOR_MAPPING, AutoImageProcessor
from transformers.models.auto.tokenization_auto import TOKENIZER_MAPPING, AutoTokenizer

from optimum.pipelines.backend import Backend


if is_torch_available():
    import torch

from .text_generation import TransformersTextGenerationPipeline
from .translation import TransformersTranslationPipeline


class TransformersBackend(Backend):
    # Those model configs are special, they are generic over their task, meaning
    # any tokenizer/feature_extractor might be use for a given model so we cannot
    # use the statically defined TOKENIZER_MAPPING and FEATURE_EXTRACTOR_MAPPING to
    # see if the model defines such objects or not.
    MULTI_MODEL_AUDIO_CONFIGS = {"SpeechEncoderDecoderConfig"}
    MULTI_MODEL_VISION_CONFIGS = {"VisionEncoderDecoderConfig", "VisionTextDualEncoderConfig"}

    SUPPORTED_TASKS = {
        "text-generation": {
            "pipeline_class": TransformersTextGenerationPipeline,
            "default_model": "openai-community/gpt2@607a30d",
            "model_class": AutoModelForCausalLM,
            "type": "text",
        },
        "translation": {
            "pipeline_class": TransformersTranslationPipeline,
            "default_model": "google-t5/t5-base@a9723ea",
            "model_class": AutoModelForSeq2SeqLM,
            "type": "text",
        },
    }

    def __init__(self):
        self.NO_FEATURE_EXTRACTOR_TASKS = set()
        self.NO_IMAGE_PROCESSOR_TASKS = set()
        self.NO_TOKENIZER_TASKS = set()
        for task, values in self.SUPPORTED_TASKS.items():
            if values["type"] == "text":
                self.NO_FEATURE_EXTRACTOR_TASKS.add(task)
                self.NO_IMAGE_PROCESSOR_TASKS.add(task)
            elif values["type"] in {"image", "video"}:
                self.NO_TOKENIZER_TASKS.add(task)
            elif values["type"] in {"audio"}:
                self.NO_TOKENIZER_TASKS.add(task)
                self.NO_IMAGE_PROCESSOR_TASKS.add(task)
            elif values["type"] != "multimodal":
                raise ValueError(f"SUPPORTED_TASK {task} contains invalid type {values['type']}")

    def get_default_model_for_task(self, task: str) -> str:
        return self.SUPPORTED_TASKS[task]["default_model"]

    def get_pipeline_for_task(self, task: str):
        return self.SUPPORTED_TASKS[task]["pipeline_class"]

    def get_model_for_task(
        self,
        task: str,
        pretrained_model_name_or_path: Union[str, Path],
        *,
        token: Optional[Union[str, bool]] = None,
        trust_remote_code: Optional[bool] = False,
        dtype: Optional[Union[str, "torch.dtype"]] = "auto",
        device: Optional[Union[int, str, "torch.device"]] = None,
    ) -> PreTrainedModel:
        if device is None:
            device = "cpu"
        if isinstance(pretrained_model_name_or_path, str):
            pretrained_model_name_or_path, revision = pretrained_model_name_or_path.split("@")
        else:
            revision = None
        return (
            self.SUPPORTED_TASKS[task]["model_class"]
            .from_pretrained(
                pretrained_model_name_or_path,
                token=token,
                trust_remote_code=trust_remote_code,
                torch_dtype=dtype,
                revision=revision,
            )
            .to(device)
        )

    def get_pipeline_init_kwargs(
        self,
        task: str,
        pretrained_model_name_or_path: Union[str, Path],
        model: PreTrainedModel,
        *,
        token: Optional[Union[str, bool]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        load_tokenizer = type(model.config) in TOKENIZER_MAPPING or model.config.tokenizer_class is not None
        load_feature_extractor = type(model.config) in FEATURE_EXTRACTOR_MAPPING
        load_image_processor = type(model.config) in IMAGE_PROCESSOR_MAPPING

        if (
            not load_tokenizer
            and task not in self.NO_TOKENIZER_TASKS
            # Using class name to avoid importing the real class.
            and (
                model.config.__class__.__name__ in self.MULTI_MODEL_AUDIO_CONFIGS
                or model.config.__class__.__name__ in self.MULTI_MODEL_VISION_CONFIGS
            )
        ):
            # This is a special category of models, that are fusions of multiple models
            # so the model_config might not define a tokenizer, but it seems to be
            # necessary for the task, so we're force-trying to load it.
            load_tokenizer = True
        if (
            not load_image_processor
            and task not in self.NO_IMAGE_PROCESSOR_TASKS
            # Using class name to avoid importing the real class.
            and model.config.__class__.__name__ in self.MULTI_MODEL_VISION_CONFIGS
        ):
            # This is a special category of models, that are fusions of multiple models
            # so the model_config might not define a tokenizer, but it seems to be
            # necessary for the task, so we're force-trying to load it.
            load_image_processor = True
        if (
            not load_feature_extractor
            and task not in self.NO_FEATURE_EXTRACTOR_TASKS
            # Using class name to avoid importing the real class.
            and model.config.__class__.__name__ in self.MULTI_MODEL_AUDIO_CONFIGS
        ):
            # This is a special category of models, that are fusions of multiple models
            # so the model_config might not define a tokenizer, but it seems to be
            # necessary for the task, so we're force-trying to load it.
            load_feature_extractor = True

        if task in self.NO_TOKENIZER_TASKS:
            # These will never require a tokenizer.
            # the model on the other hand might have a tokenizer, but
            # the files could be missing from the hub, instead of failing
            # on such repos, we just force to not load it.
            load_tokenizer = False
        if task in self.NO_FEATURE_EXTRACTOR_TASKS:
            load_feature_extractor = False
        if task in self.NO_IMAGE_PROCESSOR_TASKS:
            load_image_processor = False

        if isinstance(pretrained_model_name_or_path, str):
            pretrained_model_name_or_path, revision = pretrained_model_name_or_path.split("@")
        else:
            revision = None
        pipeline_kwargs = kwargs.copy()
        if load_tokenizer:
            tokenizer = kwargs.get("tokenizer", pretrained_model_name_or_path)
            if isinstance(tokenizer, str):
                # We always assume we can use a fast tokenizer
                tokenizer = AutoTokenizer.from_pretrained(
                    pretrained_model_name_or_path, revision=revision, token=token
                )
            pipeline_kwargs["tokenizer"] = tokenizer
        if load_image_processor:
            image_processor = kwargs.get("image_processor", pretrained_model_name_or_path)
            if isinstance(image_processor, str):
                image_processor = AutoImageProcessor.from_pretrained(
                    pretrained_model_name_or_path, revision=revision, token=token
                )
            pipeline_kwargs["image_processor"] = image_processor
        if load_feature_extractor:
            feature_extractor = kwargs.get("feature_extractor", pretrained_model_name_or_path)
            if isinstance(feature_extractor, str):
                feature_extractor = AutoFeatureExtractor.from_pretrained(
                    pretrained_model_name_or_path, revision=revision, token=token
                )
            pipeline_kwargs["feature_extractor"] = feature_extractor
        return pipeline_kwargs

    @property
    def tasks(self) -> List[str]:
        return self.SUPPORTED_TASKS.keys()
