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

import typing

from optimum.pipelines.generated.text_classification.input import TextClassificationParameters


class TextClassificationPipeline:
    def __call__(
        self,
        inputs: str,
        function_to_apply: typing.Optional[typing.Any] = None,
        top_k: typing.Optional[int] = None,
    ):
        normalized_inputs = inputs
        normalized_parameters = TextClassificationParameters(
            function_to_apply=function_to_apply,
            top_k=top_k,
        )
        return self.forward(normalized_inputs, parameters=normalized_parameters)

    def forward(self, inputs: str, parameters: TextClassificationParameters):
        raise NotImplementedError
