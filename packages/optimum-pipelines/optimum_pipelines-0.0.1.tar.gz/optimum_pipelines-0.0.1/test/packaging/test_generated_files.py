import importlib
import inspect

import pytest


def get_module_name(task):
    return task.replace("-", "_")


def test_generated_input_output(task):
    task_namespace = "optimum.pipelines.generated." + get_module_name(task)
    input_module = importlib.import_module(task_namespace + ".input")
    assert len(dir(input_module)) > 0
    output_module = importlib.import_module(task_namespace + ".output")
    assert len(dir(output_module)) > 0


def get_pipeline_class_name(task):
    task_module = get_module_name(task)
    camel_task = "".join(x.capitalize() for x in task_module.lower().split("_"))
    return camel_task + "Pipeline"


def test_generated_pipeline(task):
    pipeline_class_name = get_pipeline_class_name(task)
    generated_module = importlib.import_module("optimum.pipelines.generated")
    assert hasattr(generated_module, pipeline_class_name), f"{pipeline_class_name} not found in generated module"
    # Verify the pipeline class can be instantiated
    pipeline_class = getattr(generated_module, pipeline_class_name)
    pipe = pipeline_class()
    # Verify that calling the base pipeline class without positional args returns TypeError
    with pytest.raises(TypeError, match=r"__call__\(\) missing"):
        pipe()
    # Verify that calling the base pipeline class with expected positional args returns NotImplemented
    # For the sake of simplicity we only check here pipelines that accept a single text input
    # Each base pipeline task should have dedicated tests anyway
    sig = inspect.signature(pipe.__call__)
    if "inputs" in sig.parameters and sig.parameters["inputs"].annotation is str:
        with pytest.raises(NotImplementedError):
            pipe("foo")
