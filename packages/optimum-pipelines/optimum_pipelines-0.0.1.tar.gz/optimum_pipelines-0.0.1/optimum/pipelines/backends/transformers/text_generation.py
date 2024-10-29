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

from optimum.pipelines.generated import TextGenerationInputGenerateParameters, TextGenerationPipeline


class TransformersTextGenerationPipeline(TextGenerationPipeline):
    def __init__(self, *args, **kwargs):
        self._pipe = transformers.TextGenerationPipeline(*args, **kwargs)

    def forward(self, inputs: str, parameters: TextGenerationInputGenerateParameters):
        parameters_dict = parameters.model_dump()
        unsupported_boolean_params = ["decoder_input_details", "details", "watermark"]
        for name in unsupported_boolean_params:
            if parameters_dict[name]:
                warnings.warn(f"The {name} parameter is not supported by {self.__class__.__name__}.")
            parameters_dict.pop(name)
        unsupported_nullable_params = [
            "best_of",
            "frequency_penalty",
            "repetition_penalty",
            "grammar",
            "truncate",
            "seed",
            "stop",
            "top_n_tokens",
        ]
        for name in unsupported_nullable_params:
            if parameters_dict[name] is not None:
                warnings.warn(f"The {name} parameter is not supported by {self.__class__.__name__}.")
            parameters_dict.pop(name)
        return self._pipe(inputs, **parameters_dict)
