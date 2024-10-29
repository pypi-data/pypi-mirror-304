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

from optimum.pipelines.generated.image_segmentation.input import ImageSegmentationParameters


class ImageSegmentationPipeline:
    def __call__(
        self,
        inputs: str,
        mask_threshold: typing.Optional[float] = None,
        overlap_mask_area_threshold: typing.Optional[float] = None,
        subtask: typing.Optional[typing.Any] = None,
        threshold: typing.Optional[float] = None,
    ):
        normalized_inputs = inputs
        normalized_parameters = ImageSegmentationParameters(
            mask_threshold=mask_threshold,
            overlap_mask_area_threshold=overlap_mask_area_threshold,
            subtask=subtask,
            threshold=threshold,
        )
        return self.forward(normalized_inputs, parameters=normalized_parameters)

    def forward(self, inputs: str, parameters: ImageSegmentationParameters):
        raise NotImplementedError
