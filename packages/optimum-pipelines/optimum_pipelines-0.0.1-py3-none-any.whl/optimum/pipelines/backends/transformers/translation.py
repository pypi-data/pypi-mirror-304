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

import transformers

from optimum.pipelines.generated import TranslationParameters, TranslationPipeline


class TransformersTranslationPipeline(TranslationPipeline):
    def __init__(self, *args, **kwargs):
        self._pipe = transformers.TranslationPipeline(*args, **kwargs)

    def forward(self, inputs: str, parameters: TranslationParameters):
        parameters_dict = parameters.model_dump()
        unsupported_nullable_params = ["generate_parameters"]
        for name in unsupported_nullable_params:
            if parameters_dict[name] is not None:
                warnings.warn(f"The {name} parameter is not supported by {self.__class__.__name__}.")
            parameters_dict.pop(name)
        return self._pipe(inputs, **parameters_dict)
