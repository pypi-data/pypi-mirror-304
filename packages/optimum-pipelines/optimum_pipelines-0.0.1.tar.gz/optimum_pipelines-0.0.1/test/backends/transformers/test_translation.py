from contextlib import nullcontext

import pytest
import torch
from helpers import device_eq
from pydantic import ValidationError

from optimum.pipelines import is_transformers_available, pipeline


if is_transformers_available():
    from transformers import AutoTokenizer, T5ForConditionalGeneration

    from optimum.pipelines.backends.transformers import TransformersTranslationPipeline


def get_model_and_tokenizer():
    model_id = "patrickvonplaten/t5-tiny-random"
    model = T5ForConditionalGeneration.from_pretrained(model_id)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    return model, tokenizer


@pytest.mark.skipif(not is_transformers_available(), reason="transformers is not available")
def test_translation_inference_missing_positional(device):
    model, tokenizer = get_model_and_tokenizer()
    pipe = TransformersTranslationPipeline(model, tokenizer, device=device)
    with pytest.raises(TypeError, match=r"__call__\(\) missing 1 required positional argument: 'inputs'"):
        pipe()


@pytest.mark.skipif(not is_transformers_available(), reason="transformers is not available")
def test_translation_inference_default_parameters(device):
    model, tokenizer = get_model_and_tokenizer()
    pipe = TransformersTranslationPipeline(model, tokenizer, device=device)
    outputs = pipe("My name is David and I")
    assert len(outputs) > 0


@pytest.mark.skipif(not is_transformers_available(), reason="transformers is not available")
@pytest.mark.parametrize(
    "params, expectation",
    [
        [{"src_lang": "en"}, nullcontext()],
        [{"src_lang": 0}, pytest.raises(ValidationError, match="Input should be a valid string")],
        [{"tgt_lang": "en"}, nullcontext()],
        [{"tgt_lang": 0}, pytest.raises(ValidationError, match="Input should be a valid string")],
        [{"clean_up_tokenization_spaces": True}, nullcontext()],
        [{"clean_up_tokenization_spaces": 1}, nullcontext()],
        [
            {"clean_up_tokenization_spaces": -1},
            pytest.raises(ValidationError, match="Input should be a valid boolean"),
        ],
    ],
    ids=[
        "src-lang-correct",
        "src-lang-int",
        "tgt-lang-correct",
        "tgt-lang-int",
        "clean_up-correct",
        "clean_up-one",
        "clean_up-neg",
    ],
)
def test_translation_inference_parameters(params, expectation):
    model, tokenizer = get_model_and_tokenizer()
    pipe = TransformersTranslationPipeline(model, tokenizer, device="cpu")
    with expectation:
        pipe("My name is David and I", **params)


@pytest.mark.skipif(not is_transformers_available(), reason="transformers is not available")
def test_translation_factory_default():
    pipe = pipeline("translation", backend="transformers")
    assert isinstance(pipe, TransformersTranslationPipeline)
    outputs = pipe("My name is David and I")
    assert len(outputs) > 0


@pytest.mark.skipif(not is_transformers_available(), reason="transformers is not available")
def test_translation_factory_with_objects():
    model, tokenizer = get_model_and_tokenizer()
    pipe = pipeline("translation", backend="transformers", model=model, tokenizer=tokenizer)
    assert isinstance(pipe, TransformersTranslationPipeline)
    outputs = pipe("My name is David and I")
    assert len(outputs) > 0


@pytest.mark.skipif(not is_transformers_available(), reason="transformers is not available")
@pytest.mark.parametrize("dtype", [torch.float16, torch.bfloat16], ids=["fp16", "bf16"])
def test_translation_factory_with_device_dtype(dtype, device):
    pipe = pipeline("translation", backend="transformers", dtype=dtype, device=device)
    assert isinstance(pipe, TransformersTranslationPipeline)
    assert device_eq(pipe._pipe.model.device, device)
    assert pipe._pipe.model.dtype == dtype
    outputs = pipe("My name is David and I")
    assert len(outputs) > 0
