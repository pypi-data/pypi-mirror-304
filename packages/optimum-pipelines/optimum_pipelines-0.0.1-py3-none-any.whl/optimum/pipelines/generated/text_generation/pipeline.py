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

from annotated_types import Gt, Interval

from optimum.pipelines.generated.text_generation.input import TextGenerationInputGenerateParameters


class TextGenerationPipeline:
    def __call__(
        self,
        inputs: str,
        best_of: typing.Optional[typing.Annotated[int, None, Interval(gt=0, ge=0, lt=None, le=None), None]] = None,
        decoder_input_details: typing.Optional[bool] = False,
        details: typing.Optional[bool] = True,
        do_sample: typing.Optional[bool] = False,
        frequency_penalty: typing.Optional[
            typing.Annotated[float, None, Interval(gt=-2.0, ge=None, lt=None, le=None), None, None]
        ] = None,
        grammar: typing.Optional[typing.Any] = None,
        max_new_tokens: typing.Optional[
            typing.Annotated[int, None, Interval(gt=None, ge=0, lt=None, le=None), None]
        ] = None,
        repetition_penalty: typing.Optional[typing.Annotated[float, Gt(gt=0)]] = None,
        return_full_text: typing.Optional[bool] = None,
        seed: typing.Optional[typing.Annotated[int, None, Interval(gt=0, ge=0, lt=None, le=None), None]] = None,
        stop: typing.Optional[typing.List[str]] = None,
        temperature: typing.Optional[typing.Annotated[float, Gt(gt=0)]] = None,
        top_k: typing.Optional[typing.Annotated[int, Gt(gt=0)]] = None,
        top_n_tokens: typing.Optional[
            typing.Annotated[int, None, Interval(gt=0, ge=0, lt=None, le=None), None]
        ] = None,
        top_p: typing.Optional[
            typing.Annotated[float, None, Interval(gt=0.0, ge=None, lt=None, le=1.0), None, None]
        ] = None,
        truncate: typing.Optional[typing.Annotated[int, None, Interval(gt=None, ge=0, lt=None, le=None), None]] = None,
        typical_p: typing.Optional[
            typing.Annotated[float, None, Interval(gt=0.0, ge=None, lt=None, le=1.0), None, None]
        ] = None,
        watermark: typing.Optional[bool] = False,
    ):
        normalized_inputs = inputs
        normalized_parameters = TextGenerationInputGenerateParameters(
            best_of=best_of,
            decoder_input_details=decoder_input_details,
            details=details,
            do_sample=do_sample,
            frequency_penalty=frequency_penalty,
            grammar=grammar,
            max_new_tokens=max_new_tokens,
            repetition_penalty=repetition_penalty,
            return_full_text=return_full_text,
            seed=seed,
            stop=stop,
            temperature=temperature,
            top_k=top_k,
            top_n_tokens=top_n_tokens,
            top_p=top_p,
            truncate=truncate,
            typical_p=typical_p,
            watermark=watermark,
        )
        return self.forward(normalized_inputs, parameters=normalized_parameters)

    def forward(self, inputs: str, parameters: TextGenerationInputGenerateParameters):
        raise NotImplementedError
