from __future__ import annotations

import argparse
import importlib
import importlib.util
import os
import pathlib
import re
import sys
import warnings

from jinja2 import Template
from pydantic import BaseModel


def to_snake_case(hyphen_str):
    return hyphen_str.replace("-", "_")


def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def generate(task: str, template_file_name: str, output_file_name: str):
    """Generate the Pipeline base class for the specified task

    Args:
        task (`str`): the task to generate the Pipeline class for
        output_file_name (`str`): the name of the generated python file
    """

    snake_task = to_snake_case(task)
    camel_task = to_camel_case(snake_task)

    pipeline_module = snake_task
    pipeline_class = camel_task + "Pipeline"

    # Load the generated task module to inspect its types
    input_module_name = f"optimum.pipelines.generated.{pipeline_module}.input"
    input_module = importlib.import_module(input_module_name)

    # Load input class
    input_class_name = None
    for name in dir(input_module):
        if name.endswith("Input"):
            input_class_name = name
            break
    if input_class_name is None:
        raise ValueError("The task signature does not include a <TASK>Input class")
    input_class = getattr(input_module, input_class_name)

    # Check input class members
    if "inputs" not in input_class.model_fields:
        raise ValueError("The pipeline input signature must include an 'inputs' field")
    if "parameters" not in input_class.model_fields:
        raise ValueError("The pipeline input signature must include a 'parameters' field")

    # Look for additional parameters
    other_parameters = input_class.model_fields.copy()
    other_parameters.pop("inputs")
    other_parameters.pop("parameters")
    if len(other_parameters) > 0:
        warnings.warn(
            f"The following input parameters will be ignored when generating {pipeline_class}: {list(other_parameters.keys())}"
        )

    def get_type_from_annotation(field):
        annotation = field.annotation
        if hasattr(annotation, "__args__"):
            # Union type, typically used for optional parameter
            field_type = None
            for arg in annotation.__args__:
                if arg is not None:
                    field_type = arg
                    break
            assert field_type is not None
            return field_type
        return annotation

    inputs_field = input_class.model_fields["inputs"]
    inputs_type = get_type_from_annotation(inputs_field)
    args_lst = []
    if issubclass(inputs_type, BaseModel):
        # Flatten composite inputs into kwargs
        for name, field in inputs_type.model_fields.items():
            if isinstance(field.annotation, type):
                # Base type
                type_hint = field.annotation.__name__
            else:
                # Typing annotation
                type_hint = str(field.annotation)
                # Replace complex types by Any
                type_hint = re.sub(r"\[optimum.pipelines.generated[\.\-\w]+\]", "[typing.Any]", type_hint)
            args_lst.append((name, type_hint))
    else:
        # Use single inputs
        args_lst.append(("inputs", inputs_type.__name__))

    parameters_field = input_class.model_fields["parameters"]
    parameters_class = get_type_from_annotation(parameters_field)

    # Flatten parameters class into a list of kwargs
    kwargs_lst = []
    for name, field in parameters_class.model_fields.items():
        if field.default == "true":
            default = True
        elif field.default == "false":
            default = False
        else:
            default = None
        annotation = str(field.annotation)
        # Replace complex types by Any
        annotation = re.sub(r"\[optimum.pipelines.generated[\.\-\w]+\]", "[typing.Any]", annotation)
        kwargs_lst.append((name, annotation, default))

    pipeline_template = Template(pathlib.Path(template_file_name).read_text())
    pipeline_text = pipeline_template.render(
        pipeline_module=pipeline_module,
        pipeline_class=pipeline_class,
        args_lst=args_lst,
        inputs_type=inputs_type.__name__,
        kwargs_lst=kwargs_lst,
        parameters_class=parameters_class.__name__,
    )

    # save result to a file
    with open(output_file_name, "w") as f:
        f.write(pipeline_text)


def main():
    parser = argparse.ArgumentParser(description="Generate base Pipeline class for a task")
    parser.add_argument("task", help="The task to generate the Pipeline class for.")
    parser.add_argument("-p", "--package_root", type=str, default=None, help="The root of the package files")
    parser.add_argument("-o", "--output_file", type=str, default=None, help="The name of the generated python file.")
    args = parser.parse_args()
    current_path = os.path.dirname(os.path.realpath(__file__))
    package_root = args.package_root
    if package_root is None:
        package_root = os.path.join(current_path, "..")
    # We need to insert the root of the package files in the system path to be able
    # to load the task modules dynamically
    sys.path.insert(0, package_root)
    template_file_name = os.path.join(current_path, "pipeline.jinja")
    output_file_name = args.output_file
    if output_file_name is None:
        output_file_name = to_snake_case(args.task) + ".py"
    generate(args.task, template_file_name, output_file_name)


if __name__ == "__main__":
    main()
