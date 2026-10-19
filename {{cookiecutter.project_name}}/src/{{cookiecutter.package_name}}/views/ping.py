from typing import Annotated

from fastapi import Query
from sqlalchemy import Result, TextClause, text

from {{cookiecutter.package_name}}.__version__ import __version__
from {{cookiecutter.package_name}}.core.exceptions import Error
from {{cookiecutter.package_name}}.dependencies import DBSes
from {{cookiecutter.package_name}}.schemas.request import PingRequest
from {{cookiecutter.package_name}}.schemas.response import PingResponse


async def pong(
    query_params: Annotated[PingRequest, Query()], db: DBSes
) -> PingResponse:
    """Reply, Version as Pong"""
    if query_params.throw:
        raise Error("Raising custom exception for testing.")

    statement: TextClause = text("SELECT :version AS pong;")
    result: Result = await db.execute(statement, {"version": __version__})
    string: str = result.scalar_one()
    return PingResponse(reply=string)
