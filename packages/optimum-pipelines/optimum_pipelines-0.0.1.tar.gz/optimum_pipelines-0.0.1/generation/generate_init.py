from __future__ import annotations

import argparse
import os
import pathlib
from typing import List

from jinja2 import Template


def to_snake_case(hyphen_str):
    return hyphen_str.replace("-", "_")


def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def generate(tasks: List[str], template_file_name: str, output_file_name: str):
    """Generate the Pipeline base class for the specified task

    Args:
        tasks (`List[str]`): the list of tasks that have a Pipeline class
        template_file_name (`str`): the template to use for generation
        output_file_name (`str`): the name of the generated python file
    """

    modules_lst = [to_snake_case(task) for task in tasks]

    init_template = Template(pathlib.Path(template_file_name).read_text())
    init_text = init_template.render(tasks_lst=tasks, modules_lst=modules_lst)
    with open(output_file_name, "w") as f:
        f.write(init_text)


def main():
    parser = argparse.ArgumentParser(description="Generate __init__.py for pipeline module")
    parser.add_argument("tasks", nargs="+", help="The list of supported tasks.")
    parser.add_argument("-p", "--package_root", type=str, default=None, help="The root of the package files")
    parser.add_argument(
        "-o", "--output_file", type=str, default="__init__.py", help="The name of the generated python file."
    )
    args = parser.parse_args()
    current_path = os.path.dirname(os.path.realpath(__file__))
    template_file_name = os.path.join(current_path, "init.jinja")
    generate(args.tasks, template_file_name, args.output_file)


if __name__ == "__main__":
    main()
