# Tests for the Click command line interface

import os

from click.testing import CliRunner

from py_repo_manager import command_line_interface

test_data_path = os.path.join(os.path.dirname(__file__), "test_data/")


def test_cli():
    runner = CliRunner()
    result = runner.invoke(command_line_interface.main_group, ["--help"])
    assert result.exit_code == 0
    assert "Usage: main-group [OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Options:" in result.output
    assert "Commands:" in result.output
    assert "help" in result.output
    assert "init" in result.output
    assert "add" in result.output
    # assert "remove" in result.output
    # assert "list" in result.output
    # assert "update" in result.output
    assert "show-schema" in result.output
    # assert "sync" in result.output
    # assert "version" in result.output
    # assert "config" in result.output


def test_cli_show_schema():
    runner = CliRunner()
    result = runner.invoke(command_line_interface.main_group, ["show-schema"])
    assert result.exit_code == 0
    # assert "Usage: cli show-schema [OPTIONS]" in result.output
    # assert "Options:" in result.output
    # assert "--json" in result.output
    # assert "--yaml" in result.output
    # assert "--toml" in result.output
    # assert "--schema" in result.output
    # assert "--help" in result.output
    # assert "Show the schema for the configuration file" in result.output
