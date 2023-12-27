import sys

import click

from . import schema


@click.group()
def main_group():
    return 0


@main_group.command(name="list")
def _list():
    click.echo("list")
    return 0


@main_group.command()
def add():
    click.echo("add")
    return 0


@main_group.command()
def init():
    click.echo("init")
    return 0


@main_group.command()
def show_schema():
    click.echo("show_schema")
    schema.extract_and_print_schema()
    return 0


def main():
    return main_group()


if __name__ == "__main__":
    sys.exit(main())
