#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import importlib.resources as resources
import io
import sys

import cerberus
import rich
import ruamel.yaml
from loguru import logger

from . import line_column_utils

yaml = ruamel.yaml.YAML(typ="rt", pure=True)


def get_schema_from_pkg() -> dict:
    package_name = "py_repo_manager"
    file_name = "schema.yaml"  # Replace with your actual file path

    try:
        with resources.open_text(package_name, file_name) as file:
            return yaml.load(file.read())
    except FileNotFoundError:
        logger.error(f"File '{file_name}' not found in package '{package_name}'")


def load_schema_from_file(file_path: str) -> dict:
    with open(file_path, "r") as schema_file:
        return yaml.load(schema_file)


class LineColumnErrorHandler(cerberus.errors.BasicErrorHandler):
    def __init__(self, *args, **kwargs):
        self._errors = {}
        super().__init__(*args, **kwargs)

    def _insert_error(self, path, node):
        logger.debug(f"Error at path: {path}")
        logger.debug(f"Error at node: {node}")
        path_name = ".".join(str(item) for item in tuple(path))
        if path_name in self._errors:
            self._errors[path_name].append(node)
        else:
            self._errors[path_name] = [node]
        super()._insert_error(path, node)

    @property
    def all_errors(self):
        return self._errors


def validate_configuration(
    config_file: str, schema: dict = None, print_errors=True
) -> bool:
    schema = schema or get_schema_from_pkg()
    v = cerberus.Validator(schema, error_handler=LineColumnErrorHandler())

    with open(config_file, "r") as config:
        cfg = yaml.load(config)

    is_valid = v.validate(cfg)
    # Dummy invoke of errors to populate error_handler
    _ = v.errors

    if is_valid:
        return True
    else:
        if not print_errors:
            return False
        errors_at_line = {}
        for key, value in v.error_handler.all_errors.items():
            try:
                lc = line_column_utils.get_lc(cfg, key)
                errors_at_line[lc.line] = value
            except KeyError as e:
                if "required field" in str(value):
                    if "." in key:
                        top_key = ".".join(key.rsplit(".", 1)[:-1])
                        lc = line_column_utils.get_lc(cfg, top_key)
                        errors_at_line[lc.line] = value
                else:
                    raise e
        yaml_content = io.StringIO()
        yaml.dump(cfg, yaml_content)
        yaml_lines = yaml_content.getvalue().splitlines()

        for index, line in enumerate(yaml_lines, start=0):
            if index in errors_at_line:
                rich.print(f"[red]{index+1:3d} {line}[/red]")
                for error in errors_at_line[index]:
                    rich.print(
                        rich.panel.Panel.fit(
                            "[red]" + error, title="[reverse red]Error"
                        )
                    )
            else:
                rich.print(f"{index+1:3d} {line}")
        return False


def extract_and_print_schema() -> None:
    schema = get_schema_from_pkg()
    yaml.dump(schema, sys.stdout)
