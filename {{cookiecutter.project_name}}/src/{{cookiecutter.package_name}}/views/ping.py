from sqlalchemy import Result, TextClause, text
from sqlalchemy.ext.asyncio import AsyncSession

from {{cookiecutter.package_name}}.dependencies import DBSes
from {{cookiecutter.package_name}}.schemas.response import Pong


async def pong(db: AsyncSession = DBSes) -> Pong:
    """Reply, Pong"""
    statement: TextClause = text("SELECT 'Pong' AS pong;")
    result: Result = await db.execute(statement)
    string: str = result.scalar_one()
    return Pong(reply=string)
