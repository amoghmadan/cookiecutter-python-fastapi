from sqlalchemy import Result, TextClause, text

from {{cookiecutter.package_name}}.__version__ import __version__
from {{cookiecutter.package_name}}.dependencies import DBSes
from {{cookiecutter.package_name}}.schemas.response import Pong


async def pong(db: DBSes) -> Pong:
    """Reply, Version as Pong"""
    statement: TextClause = text("SELECT :version AS pong;")
    result: Result = await db.execute(statement, {"version": __version__})
    string: str = result.scalar_one()
    return Pong(reply=string)
