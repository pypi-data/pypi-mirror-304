"""Create, manage, and run reproducible Jupyter notebooks."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import click
import rich


@click.group()
@click.version_option()
def cli() -> None:
    """Create, manage, and run reproducible Jupyter notebooks."""


@cli.command()
@click.option("--detail", is_flag=True)
def version(*, detail: bool) -> None:
    """Display juv's version."""
    from ._version import __version__

    print(f"juv v{__version__}")  # noqa: T201

    if detail:
        from ._uv import uv

        uv(["version"], check=True)


@cli.command()
@click.argument("file", type=click.Path(exists=False), required=False)
@click.option("--with", "with_args", type=click.STRING, multiple=True)
@click.option("--python", type=click.STRING, required=False)
def init(
    file: str | None,
    with_args: tuple[str, ...],
    python: str | None,
) -> None:
    """Initialize a new notebook."""
    from ._init import init

    path = init(
        path=Path(file) if file else None,
        python=python,
        packages=[p for w in with_args for p in w.split(",")],
    )
    path = os.path.relpath(path.resolve(), Path.cwd())
    rich.print(f"Initialized notebook at `[cyan]{path}[/cyan]`")


@cli.command()
@click.argument("file", type=click.Path(exists=True), required=True)
@click.option("--requirements", "-r", type=click.Path(exists=True), required=False)
@click.argument("packages", nargs=-1)
def add(file: str, requirements: str | None, packages: tuple[str, ...]) -> None:
    """Add dependencies to the notebook."""
    from ._add import add

    add(path=Path(file), packages=packages, requirements=requirements)
    path = os.path.relpath(Path(file).resolve(), Path.cwd())
    rich.print(f"Updated `[cyan]{path}[/cyan]`")


@cli.command()
@click.argument("file", type=click.Path(exists=True), required=True)
@click.option(
    "--jupyter",
    required=False,
    help="The Jupyter frontend to use. [env: JUV_JUPYTER=]",
)
@click.option("--with", "with_args", type=click.STRING, multiple=True)
@click.option("--python", type=click.STRING, required=False)
def run(
    file: str,
    jupyter: str | None,
    with_args: tuple[str, ...],
    python: str | None,
) -> None:
    """Launch a notebook or script."""
    from ._run import run

    run(
        path=Path(file),
        jupyter=jupyter,
        python=python,
        with_args=with_args,
    )


def upgrade_legacy_jupyter_command(args: list[str]) -> None:
    """Check legacy command usage and upgrade to 'run' with deprecation notice."""
    if len(args) >= 2:  # noqa: PLR2004
        command = args[1]
        if command.startswith(("lab", "notebook", "nbclassic")):
            rich.print(
                f"[bold]Warning:[/bold] The command '{command}' is deprecated. "
                f"Please use 'run' with `--jupyter={command}` "
                f"or set JUV_JUPYTER={command}",
            )
            os.environ["JUV_JUPYTER"] = command
            args[1] = "run"


def main() -> None:
    """Run the CLI."""
    upgrade_legacy_jupyter_command(sys.argv)
    cli()
