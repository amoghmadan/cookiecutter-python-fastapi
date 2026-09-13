from typing import Annotated

import typer

from {{cookiecutter.package_name}}.__version__ import __version__
from {{cookiecutter.package_name}}.conf import settings
from {{cookiecutter.package_name}}.core.management.commands import commands


def verbose_callback(ctx: typer.Context, value: bool) -> None:
    """Callback: Version"""
    if value and not ctx.invoked_subcommand:
        raise typer.Exit()


def version_callback(ctx: typer.Context, value: bool) -> None:
    """Callback: Version"""
    if value and not ctx.invoked_subcommand:
        if not isinstance(__package__, str):
            raise typer.Exit()
        typer.echo(f"{__package__.split('.')[0]}, {__version__}")
        raise typer.Exit()


execute_from_command_line = typer.Typer(add_completion=False)


@execute_from_command_line.callback()
def main(
    ctx: typer.Context,
    verbose: Annotated[
        int,
        typer.Option(
            "--verbose",
            "-v",
            help="Increase verbosity (-v, -vv).",
            callback=verbose_callback,
            count=True,
            is_eager=True,
        ),
    ] = 0,
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Show the application's version and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = False,
):
    """Manage the awesome CLI application."""
    ctx.ensure_object(dict)
    ctx.obj.update(
        debug=settings.DEBUG,
        verbose=verbose,
        version=version,
    )


for command in commands:
    execute_from_command_line.add_typer(command)

__all__ = ["execute_from_command_line"]
