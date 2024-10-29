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

from optimum.pipelines.generated.text_to_image.input import TextToImageParameters


class TextToImagePipeline:
    def __call__(
        self,
        inputs: str,
        guidance_scale: typing.Optional[float] = None,
        negative_prompt: typing.Optional[typing.List[str]] = None,
        num_inference_steps: typing.Optional[int] = None,
        target_size: typing.Optional[typing.Any] = None,
        scheduler: typing.Optional[str] = None,
        seed: typing.Optional[int] = None,
    ):
        normalized_inputs = inputs
        normalized_parameters = TextToImageParameters(
            guidance_scale=guidance_scale,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inference_steps,
            target_size=target_size,
            scheduler=scheduler,
            seed=seed,
        )
        return self.forward(normalized_inputs, parameters=normalized_parameters)

    def forward(self, inputs: str, parameters: TextToImageParameters):
        raise NotImplementedError
