import asyncio
import importlib
import json
from typing import Annotated, Any

import typer
from sqlalchemy.exc import IntegrityError

from {{cookiecutter.package_name}}.conf import settings
from {{cookiecutter.package_name}}.db import session

cli = typer.Typer()


async def _process(data: list[dict[str, Any]]) -> None:
    async with session() as db:
        for entry in data:
            try:
                model_name = entry.pop("model").split(".")[-1]
                model_module = importlib.import_module("{{cookiecutter.package_name}}.models")
                model_class = getattr(model_module, model_name)
                obj = model_class(id=entry["pk"], **entry["fields"])
                db.add(obj)
                await db.commit()
            except IntegrityError:
                await db.rollback()


@cli.command()
def loaddata(
    ctx: typer.Context,
    files: Annotated[list[str], typer.Option(help="Fixture files.")],
) -> None:
    """Load JSON data into tables."""
    fixtures_dir = settings.BASE_DIR.parent / "fixtures"  # type: ignore[attr-defined]
    for file in files:
        with open(fixtures_dir / file, "r") as fp:
            data = json.load(fp)
        asyncio.run(_process(data))
