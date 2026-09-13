import code
import os
import sys
from typing import Any

import typer

cli = typer.Typer()


def get_namespace(no_imports: bool) -> dict[str, Any]:
    """Generates the context namespace for the interactive shell."""
    if no_imports:
        return {}

    # Define the default objects you want loaded in your application context
    namespace: dict[str, Any] = {
        "os": os,
        "sys": sys,
    }
    return namespace


def launch_ipython(namespace: dict[str, Any]) -> None:
    """Launches an IPython interactive shell."""
    from IPython import start_ipython  # ty: ignore[unresolved-import]

    start_ipython(argv=[], user_ns=namespace)


def launch_bpython(namespace: dict[str, Any]) -> None:
    """Launches a bpython interactive shell."""
    import bpython  # ty: ignore[unresolved-import]

    bpython.embed(namespace)


def launch_python(namespace: dict[str, Any], no_startup: bool) -> None:
    """Launches the standard plain Python interactive shell."""
    # Process startup files if requested
    if not no_startup:
        for pythonrc in [
            os.environ.get("PYTHONSTARTUP"),
            os.path.expanduser("~/.pythonrc.py"),
        ]:
            if pythonrc and os.path.isfile(pythonrc):
                try:
                    with open(pythonrc) as f:
                        exec(compile(f.read(), pythonrc, "exec"), namespace)  # noqa: S102  # nosec
                except Exception as e:  # noqa: BLE001
                    print(
                        f"Error loading startup file {pythonrc}: {e}", file=sys.stderr
                    )

    # Enable tab completion
    try:
        import readline
        import rlcompleter

        readline.set_completer(rlcompleter.Completer(namespace).complete)
        readline.parse_and_bind("tab: complete")
    except ImportError:
        pass

    # Drop into the native Python REPL using the constructed context
    code.interact(local=namespace)


@cli.command()
def shell(
    ctx: typer.Context,
    interface: str | None = typer.Option(
        None,
        "-i",
        "--interface",
        help="Specify an interactive interpreter interface. Options: 'ipython', 'bpython', 'python'.",
    ),
    no_imports: bool = typer.Option(
        False,
        "--no-imports",
        help="Disable automatic imports of application context objects.",
    ),
    no_startup: bool = typer.Option(
        False,
        "--no-startup",
        help="When using plain Python, ignore the PYTHONSTARTUP environment variable and ~/.pythonrc.py script.",
    ),
    command: str | None = typer.Option(
        None,
        "-c",
        "--command",
        help="Instead of opening an interactive shell, run a command string and exit.",
    ),
) -> None:
    """Python shell with application context."""
    # 1. Build the shell environment namespace
    namespace = get_namespace(no_imports)

    # 2. If a specific inline command is given, run it immediately and exit
    if command:
        exec(command, globals(), namespace)  # noqa: S102  # nosec
        return

    # 3. Determine which shells to try based on user choices
    shells = [interface] if interface else ["ipython", "bpython", "python"]

    for shell_name in shells:
        try:
            if shell_name == "ipython":
                launch_ipython(namespace)
                return
            elif shell_name == "bpython":
                launch_bpython(namespace)
                return
            elif shell_name == "python":
                launch_python(namespace, no_startup)
                return
        except ImportError:
            # If the selected custom shell isn't installed, try the next fallback
            if interface:
                typer.echo(
                    f"Error: Couldn't import '{shell_name}' interface.", err=True
                )
                raise typer.Exit(code=1)
            continue
