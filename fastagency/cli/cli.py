from logging import getLogger
from pathlib import Path
from typing import Annotated, Any, Optional

import typer

from .. import __version__
from ..exceptions import FastAgencyCLIError, FastAgencyCLIPythonVersionError
from .discover import get_import_string
from .docker_cli import docker_app
from .logging import setup_logging

app = typer.Typer(rich_markup_mode="rich")
app.add_typer(
    docker_app,
    name="docker",
    help="[bold]Docker[/bold] commands for [bold]FastAgency[/bold]",
)

setup_logging()
logger = getLogger(__name__)


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__version__}")
        raise typer.Exit()


@app.callback()
def callback(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version", help="Show the version and exit.", callback=version_callback
        ),
    ] = None,
) -> None:
    """FastAgency CLI - The [bold]fastapi[/bold] command line app. 😎

    Manage your [bold]FastAgency[/bold] projects, run your FastAgency apps, and more.

    Read more in the docs: [link]https://fastagency.ai/latest/[/link].
    """  # noqa: D415


def _run_app(
    *,
    path: Optional[Path],
    app: Optional[str],
    workflow: Optional[str],
    params: dict[str, Any],
    dev_mode: bool = False,
    single_run: bool = False,
) -> None:
    try:
        import_string, fa_app = get_import_string(path=path, app_name=app)

        with fa_app.create(import_string=import_string):
            fa_app.start(
                import_string=import_string,
                name=workflow,
                params=params,
                single_run=single_run,
            )
    except FastAgencyCLIPythonVersionError as e:
        msg = e.args[0]
        typer.echo(msg, err=True)
        raise typer.Exit(code=1)  # noqa: B904
    except FastAgencyCLIError as e:
        msg = e.args[0]
        typer.echo(msg, err=True)
        raise typer.Exit(code=1) from None


def _get_help_messages(dev_mode: bool = False) -> dict[str, str]:
    help = f"""Run a [bold]FastAgency[/bold] app in [yellow]{'development' if dev_mode else 'production'}[/yellow] mode. 🚀

{'This is similar to the [bold]fastagency run[/bold] command but with [bold]reload[/bold] enabled and listening on the [blue]127.0.0.1[/blue] address.' if dev_mode else 'This is similar to the [bold]fastagency dev[/bold] command, but optimized for production environments.'}

It automatically detects the Python module or package that needs to be imported based on the file or directory path passed.

If no path is passed, it tries with:

- [blue]main.py[/blue]
- [blue]app.py[/blue]
- [blue]api.py[/blue]
- [blue]app/main.py[/blue]
- [blue]app/app.py[/blue]
- [blue]app/api.py[/blue]

It also detects the directory that needs to be added to the [bold]PYTHONPATH[/bold] to make the app importable and adds it.

It detects the [bold]FastAgency[/bold] app object to use. By default it looks in the module or package for an object named:

- [blue]app[/blue]
- [blue]api[/blue]

Otherwise, it uses the first [bold]FastAgency[/bold] app found in the imported module or package.
"""
    short_help = f"Run a [bold]FastAgency[/bold] app in [yellow]{'development' if dev_mode else 'production'}[/yellow] mode."
    return {"help": help, "short_help": short_help}


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    **_get_help_messages(False),  # type: ignore[arg-type]
)
def run(
    path: Annotated[
        Optional[Path],
        typer.Argument(
            help="A path to a Python file or package directory (with [blue]__init__.py[/blue] files) containing a [bold]FastAgency[/bold] app. If not provided, a default set of paths will be tried."
        ),
    ] = None,
    *,
    app: Annotated[
        Optional[str],
        typer.Option(
            help="The name of the variable that contains the [bold][/bold] app in the imported module or package. If not provided, it is detected automatically."
        ),
    ] = None,
    workflow: Annotated[
        Optional[str],
        typer.Option(
            "--workflow",
            "-w",
            help="The name of the workflow to run. If not provided, the default workflow will be run.",
        ),
    ] = None,
    single_run: Annotated[
        bool,
        typer.Option(
            "--single-run", help="If set, only a single workflow will be executed."
        ),
    ] = False,
    ctx: typer.Context,
) -> None:
    if len(ctx.args) > 0:
        raise NotImplementedError("Extra arguments are not supported in this command.")
    else:
        params: dict[str, Any] = {}

    dev_mode = False
    _run_app(
        path=path,
        app=app,
        workflow=workflow,
        params=params,
        dev_mode=dev_mode,
        single_run=single_run,
    )


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    **_get_help_messages(True),  # type: ignore[arg-type]
)
def dev(
    path: Annotated[
        Optional[Path],
        typer.Argument(
            help="A path to a Python file or package directory (with [blue]__init__.py[/blue] files) containing a [bold]FastAgency[/bold] app. If not provided, a default set of paths will be tried."
        ),
    ] = None,
    *,
    app: Annotated[
        Optional[str],
        typer.Option(
            help="The name of the variable that contains the [bold][/bold] app in the imported module or package. If not provided, it is detected automatically."
        ),
    ] = None,
    workflow: Annotated[
        Optional[str],
        typer.Option(
            "--workflow",
            "-w",
            help="The name of the workflow to run. If not provided, the default workflow will be run.",
        ),
    ] = None,
    single_run: Annotated[
        bool,
        typer.Option(
            "--single-run", help="If set, only a single workflow will be executed."
        ),
    ] = False,
    ctx: typer.Context,
) -> None:
    dev_mode = True
    if len(ctx.args) > 0:
        raise NotImplementedError("Extra arguments are not supported in this command.")
    else:
        params: dict[str, Any] = {}
    _run_app(
        path=path,
        app=app,
        workflow=workflow,
        params=params,
        dev_mode=dev_mode,
        single_run=single_run,
    )


@app.command(help="Display the version of FastAgency")
def version() -> None:
    typer.echo(__version__)


def main() -> None:
    app()
