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

from optimum.pipelines.generated.visual_question_answering.input import Inputs, VisualQuestionAnsweringParameters


class VisualQuestionAnsweringPipeline:
    def __call__(
        self,
        image: typing.Any,
        question: typing.Any,
        top_k: typing.Optional[int] = None,
    ):
        normalized_inputs = Inputs(
            image=image,
            question=question,
        )
        normalized_parameters = VisualQuestionAnsweringParameters(
            top_k=top_k,
        )
        return self.forward(normalized_inputs, parameters=normalized_parameters)

    def forward(self, inputs: Inputs, parameters: VisualQuestionAnsweringParameters):
        raise NotImplementedError
