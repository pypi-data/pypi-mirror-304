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

from optimum.pipelines.generated.question_answering.input import Inputs, QuestionAnsweringParameters


class QuestionAnsweringPipeline:
    def __call__(
        self,
        context: str,
        question: str,
        top_k: typing.Optional[int] = None,
        doc_stride: typing.Optional[int] = None,
        max_answer_len: typing.Optional[int] = None,
        max_seq_len: typing.Optional[int] = None,
        max_question_len: typing.Optional[int] = None,
        handle_impossible_answer: typing.Optional[bool] = None,
        align_to_words: typing.Optional[bool] = None,
    ):
        normalized_inputs = Inputs(
            context=context,
            question=question,
        )
        normalized_parameters = QuestionAnsweringParameters(
            top_k=top_k,
            doc_stride=doc_stride,
            max_answer_len=max_answer_len,
            max_seq_len=max_seq_len,
            max_question_len=max_question_len,
            handle_impossible_answer=handle_impossible_answer,
            align_to_words=align_to_words,
        )
        return self.forward(normalized_inputs, parameters=normalized_parameters)

    def forward(self, inputs: Inputs, parameters: QuestionAnsweringParameters):
        raise NotImplementedError
