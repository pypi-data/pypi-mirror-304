from contextlib import nullcontext

import pytest
import torch
from pydantic import ValidationError

from optimum.pipelines import is_transformers_available, pipeline


if is_transformers_available():
    from transformers import AutoModelForCausalLM, AutoTokenizer

    from optimum.pipelines.backends.transformers import TransformersTextGenerationPipeline


def get_model_and_tokenizer():
    model_id = "hf-internal-testing/tiny-random-gpt2"
    model = AutoModelForCausalLM.from_pretrained(model_id)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    return model, tokenizer


@pytest.mark.skipif(not is_transformers_available(), reason="transformers is not available")
def test_text_generation_inference_missing_positional(device):
    model, tokenizer = get_model_and_tokenizer()
    pipe = TransformersTextGenerationPipeline(model, tokenizer, device=device)
    with pytest.raises(TypeError, match=r"__call__\(\) missing 1 required positional argument: 'inputs'"):
        pipe()


@pytest.mark.skipif(not is_transformers_available(), reason="transformers is not available")
def test_text_generation_inference_default_parameters(device):
    model, tokenizer = get_model_and_tokenizer()
    pipe = TransformersTextGenerationPipeline(model, tokenizer, device=device)
    outputs = pipe("My name is David and I")
    assert len(outputs) > 0


@pytest.mark.skipif(not is_transformers_available(), reason="transformers is not available")
@pytest.mark.parametrize(
    "params, expectation",
    [
        [{"do_sample": True, "top_k": 50}, nullcontext()],
        [{"do_sample": True, "top_k": -1}, pytest.raises(ValidationError, match="Input should be greater than 0")],
        [{"do_sample": True, "top_k": 0}, pytest.raises(ValidationError, match="Input should be greater than 0")],
        [{"do_sample": True, "top_k": 1.1}, pytest.raises(ValidationError, match="Input should be a valid integer")],
        [{"do_sample": True, "top_p": 0.9}, nullcontext()],
        [{"do_sample": True, "top_p": -1}, pytest.raises(ValidationError, match="Input should be greater than 0")],
        [{"do_sample": True, "top_p": 0}, pytest.raises(ValidationError, match="Input should be greater than 0")],
        [
            {"do_sample": True, "top_p": 2.0},
            pytest.raises(ValidationError, match="Input should be less than or equal to 1"),
        ],
    ],
    ids=[
        "top_k-correct",
        "top_k-neg",
        "top_k-zero",
        "top_k-float",
        "top_p-correct",
        "top_p-neg",
        "top_p-zero",
        "top_p-int",
    ],
)
def test_text_generation_inference_parameters(params, expectation):
    model, tokenizer = get_model_and_tokenizer()
    pipe = TransformersTextGenerationPipeline(model, tokenizer, device="cpu")
    with expectation:
        pipe("My name is David and I", **params)


@pytest.mark.skipif(not is_transformers_available(), reason="transformers is not available")
def test_text_generation_factory_default():
    pipe = pipeline("text-generation", backend="transformers")
    assert isinstance(pipe, TransformersTextGenerationPipeline)
    outputs = pipe("My name is David and I")
    assert len(outputs) > 0


@pytest.mark.skipif(not is_transformers_available(), reason="transformers is not available")
def test_text_generation_factory_with_objects():
    model, tokenizer = get_model_and_tokenizer()
    pipe = pipeline("text-generation", backend="transformers", model=model, tokenizer=tokenizer)
    assert isinstance(pipe, TransformersTextGenerationPipeline)
    outputs = pipe("My name is David and I")
    assert len(outputs) > 0


@pytest.mark.skipif(not is_transformers_available(), reason="transformers is not available")
@pytest.mark.parametrize("dtype", [torch.float16, torch.bfloat16], ids=["fp16", "bf16"])
def test_text_generation_factory_with_device_dtype(dtype, device):
    pipe = pipeline("text-generation", backend="transformers", dtype=dtype, device=device)
    assert isinstance(pipe, TransformersTextGenerationPipeline)
    outputs = pipe("My name is David and I")
    assert len(outputs) > 0
    assert pipe._pipe.model.dtype == dtype
