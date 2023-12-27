#!/usr/bin/env python3


import cerberus
import line_column_utils
import ruamel.yaml
from loguru import logger

yaml = ruamel.yaml.YAML(typ="rt", pure=True)


def load_schema_from_file(file_path: str) -> dict:
    with open(file_path, "r") as schema_file:
        return yaml.load(schema_file)


def validate_configuration(config_file: dict, schema: dict = None) -> bool:
    schema = schema or load_schema_from_file("schema.yaml")
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
