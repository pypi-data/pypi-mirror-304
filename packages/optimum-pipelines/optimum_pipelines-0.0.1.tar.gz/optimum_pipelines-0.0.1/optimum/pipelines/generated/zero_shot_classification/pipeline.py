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

from optimum.pipelines.generated.zero_shot_classification.input import Inputs, ZeroShotClassificationParameters


class ZeroShotClassificationPipeline:
    def __call__(
        self,
        text: str,
        candidateLabels: typing.List[str],
        hypothesis_template: typing.Optional[str] = None,
        multi_label: typing.Optional[bool] = None,
    ):
        normalized_inputs = Inputs(
            text=text,
            candidateLabels=candidateLabels,
        )
        normalized_parameters = ZeroShotClassificationParameters(
            hypothesis_template=hypothesis_template,
            multi_label=multi_label,
        )
        return self.forward(normalized_inputs, parameters=normalized_parameters)

    def forward(self, inputs: Inputs, parameters: ZeroShotClassificationParameters):
        raise NotImplementedError
