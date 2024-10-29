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

from optimum.pipelines.generated.document_question_answering.input import DocumentQuestionAnsweringParameters, Inputs


class DocumentQuestionAnsweringPipeline:
    def __call__(
        self,
        image: typing.Any,
        question: str,
        doc_stride: typing.Optional[int] = None,
        handle_impossible_answer: typing.Optional[bool] = None,
        lang: typing.Optional[str] = None,
        max_answer_len: typing.Optional[int] = None,
        max_seq_len: typing.Optional[int] = None,
        max_question_len: typing.Optional[int] = None,
        top_k: typing.Optional[int] = None,
        word_boxes: typing.Optional[typing.List[typing.Union[str, typing.List[float]]]] = None,
    ):
        normalized_inputs = Inputs(
            image=image,
            question=question,
        )
        normalized_parameters = DocumentQuestionAnsweringParameters(
            doc_stride=doc_stride,
            handle_impossible_answer=handle_impossible_answer,
            lang=lang,
            max_answer_len=max_answer_len,
            max_seq_len=max_seq_len,
            max_question_len=max_question_len,
            top_k=top_k,
            word_boxes=word_boxes,
        )
        return self.forward(normalized_inputs, parameters=normalized_parameters)

    def forward(self, inputs: Inputs, parameters: DocumentQuestionAnsweringParameters):
        raise NotImplementedError
