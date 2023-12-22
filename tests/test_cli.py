# Tests for the Click command line interface

from click.testing import CliRunner

from py_repo_manager.cli import cli


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage: cli [OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Options:" in result.output
    assert "Commands:" in result.output
    assert "help" in result.output
    assert "init" in result.output
    assert "add" in result.output
    assert "remove" in result.output
    assert "list" in result.output
    assert "update" in result.output
    assert "show" in result.output
    assert "sync" in result.output
    assert "version" in result.output
    assert "config" in result.output
