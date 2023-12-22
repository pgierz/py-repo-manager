import sys
import click


@click.group()
def cli():
    return 0


@cli.command(name="list")
def _list():
    click.echo("list")
    return 0


@cli.command()
def add():
    click.echo("add")
    return 0


@cli.command()
def init():
    click.echo("init")
    return 0


def main():
    return cli()
    return 0


if __name__ == "__main__":
    sys.exit(main())
