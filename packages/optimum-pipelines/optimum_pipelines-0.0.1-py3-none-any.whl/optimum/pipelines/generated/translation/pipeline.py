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

from optimum.pipelines.generated.translation.input import TranslationParameters


class TranslationPipeline:
    def __call__(
        self,
        inputs: str,
        src_lang: typing.Optional[str] = None,
        tgt_lang: typing.Optional[str] = None,
        clean_up_tokenization_spaces: typing.Optional[bool] = None,
        truncation: typing.Optional[typing.Any] = None,
        generate_parameters: typing.Optional[typing.Dict[str, typing.Any]] = None,
    ):
        normalized_inputs = inputs
        normalized_parameters = TranslationParameters(
            src_lang=src_lang,
            tgt_lang=tgt_lang,
            clean_up_tokenization_spaces=clean_up_tokenization_spaces,
            truncation=truncation,
            generate_parameters=generate_parameters,
        )
        return self.forward(normalized_inputs, parameters=normalized_parameters)

    def forward(self, inputs: str, parameters: TranslationParameters):
        raise NotImplementedError
