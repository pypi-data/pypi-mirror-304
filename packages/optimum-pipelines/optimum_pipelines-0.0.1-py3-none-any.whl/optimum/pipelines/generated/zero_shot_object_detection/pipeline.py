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

from optimum.pipelines.generated.zero_shot_object_detection.input import Inputs, ZeroShotObjectDetectionParameters


class ZeroShotObjectDetectionPipeline:
    def __call__(
        self,
        image: typing.Any,
        candidateLabels: typing.List[str],
    ):
        normalized_inputs = Inputs(
            image=image,
            candidateLabels=candidateLabels,
        )
        normalized_parameters = ZeroShotObjectDetectionParameters()
        return self.forward(normalized_inputs, parameters=normalized_parameters)

    def forward(self, inputs: Inputs, parameters: ZeroShotObjectDetectionParameters):
        raise NotImplementedError
