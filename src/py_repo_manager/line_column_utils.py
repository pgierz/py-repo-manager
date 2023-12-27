import sys
from typing import NamedTuple

import dpath.util
import ruamel.yaml as yaml
from loguru import logger

yaml = yaml.YAML(typ="rt")

data_location = NamedTuple(
    "data_location", [("line", int), ("col", int), ("prefix", str)]
)


def get_lc(data, prefix=""):
    if prefix:
        original_data = data
        data = dpath.get(data, prefix, separator=".")
    if hasattr(data, "lc"):
        logger.debug(f"Data up to {prefix} has line/column information")
        logger.debug(f"{prefix=} is at line/column: {data.lc.line}:{data.lc.col}")
        return data_location(
            line=data.lc.line,
            col=data.lc.col,
            prefix=prefix,
        )
    else:
        logger.debug(
            f"Data up to {prefix} does not have direct line/column information"
        )
        logger.debug("Restoring original data without removing prefix")
        data = original_data
        prefix_minus_last, last = prefix.rsplit(".", 1)
        logger.debug(f"{prefix_minus_last=}, {last=}")
        if prefix_minus_last.startswith("."):
            # Remove very first dot at beginning of prefix
            prefix_minus_last = prefix_minus_last[1:]
        data_above = dpath.get(data, prefix_minus_last, separator=".")
        # Check if we have a dict or list:
        if isinstance(data_above, dict):
            try:
                logger.debug(data_above.lc.key(last))
                return data_location(
                    line=data_above.lc.key(last)[0],
                    col=data_above.lc.key(last)[1],
                    prefix=prefix,
                )
            except AttributeError:
                raise AttributeError("Line/column information not available")
            except KeyError:
                raise KeyError(f"The {prefix=} does not exist in the data")
        elif isinstance(data_above, list):
            try:
                logger.debug(data_above.lc.item(last))
                return data_location(
                    line=data_above.lc.item(last)[0],
                    col=data_above.lc.item(last)[1],
                    prefix=prefix,
                )
            except AttributeError:
                raise AttributeError("Line/column information not available")
            except KeyError:
                raise KeyError(f"The {prefix=} does not exist in the data")
        else:
            raise TypeError(
                f"Data above {prefix=} is not a dict or list, but a {type(data_above)}"
            )


def get_all_lc(data, prefix=""):
    lc_data = {}
    if isinstance(data, dict):
        for key, value in data.items():
            # lc_data[key] = get_lc(data, prefix=f"{prefix}.{key}")
            # Recurse inwards
            lc_data[key] = get_all_lc(value, prefix=f"{prefix}.{key}")
    elif isinstance(data, list):
        for index, value in enumerate(data):
            lc_data[index] = get_all_lc(value, prefix=f"{prefix}[{index}]")
    else:
        lc_data[prefix] = get_lc(data, prefix=prefix)
    return lc_data


def get_line_column_from_above(data, prefix):
    prefix_minus_last, last = prefix.rsplit(".", 1)
    if prefix_minus_last.startswith("."):
        # Remove very first dot at beginning of prefix
        prefix_minus_last = prefix_minus_last[1:]
    data_above = dpath.get(data, prefix_minus_last, separator=".")
    try:
        print(data_above.lc.key(last), data_above.lc.value(last))
    except AttributeError:
        print(
            f"Could not get line/column information for {prefix_minus_last} and {last}"
        )


def main():
    with open("input_file.yaml", "r") as f:
        data = yaml.load(f)
    out = get_all_lc(data)
    print(out)

    sys.exit(0)


if __name__ == "__main__":
    main()
