#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import importlib.resources as resources
import sys

import cerberus
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


def validate_configuration(config_file: dict, schema: dict = None) -> bool:
    schema = schema or get_schema_from_pkg()
    v = cerberus.Validator(schema)

    with open(config_file, "r") as config:
        cfg = yaml.load(config)

    if v.validate(cfg):
        return True
    else:
        for error in v._errors:
            line, column, prefix = line_column_utils.get_all_lc(
                cfg, ".".join(error.document_path)
            )
            logger.debug(f"{line=}, {column=}, {prefix=}")
        return False


def extract_and_print_schema() -> None:
    schema = get_schema_from_pkg()
    yaml.dump(schema, sys.stdout)
