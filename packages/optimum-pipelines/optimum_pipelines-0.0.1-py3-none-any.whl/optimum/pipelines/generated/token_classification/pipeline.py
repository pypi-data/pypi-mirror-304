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

from optimum.pipelines.generated.token_classification.input import TokenClassificationParameters


class TokenClassificationPipeline:
    def __call__(
        self,
        inputs: str,
        ignore_labels: typing.Optional[typing.List[str]] = None,
        stride: typing.Optional[int] = None,
        aggregation_strategy: typing.Optional[str] = None,
    ):
        normalized_inputs = inputs
        normalized_parameters = TokenClassificationParameters(
            ignore_labels=ignore_labels,
            stride=stride,
            aggregation_strategy=aggregation_strategy,
        )
        return self.forward(normalized_inputs, parameters=normalized_parameters)

    def forward(self, inputs: str, parameters: TokenClassificationParameters):
        raise NotImplementedError
