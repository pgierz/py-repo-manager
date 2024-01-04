import os

import pytest
import ruamel.yaml

from py_repo_manager import schema

test_data_path = os.path.join(os.path.dirname(__file__), "test_data/")

yaml = ruamel.yaml.YAML(typ="rt")


@pytest.fixture
def broken_yaml():
    with open(test_data_path + "broken_scratch.yaml", "r") as f:
        return yaml.load(f)


def test_broken_yaml(capfd):
    out = schema.validate_configuration(f"{test_data_path}/broken_scratch.yaml")
    stdout, stderr = capfd.readouterr()
    assert "required field" in stdout
    assert "╭──── Error ─────╮" in stdout
    assert out is False
