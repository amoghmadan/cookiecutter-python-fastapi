import typer
import uvicorn

cli = typer.Typer()


@cli.command()
def runserver(ctx: typer.Context, host: str = "127.0.0.1", port: int = 8000) -> None:
    """Run server."""
    uvicorn.run("{{cookiecutter.package_name}}.asgi:application", host=host, port=port, reload=ctx.obj["debug"])
