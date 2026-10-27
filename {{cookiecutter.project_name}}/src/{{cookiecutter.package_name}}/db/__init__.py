from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from {{cookiecutter.package_name}}.db.engines import engines
from {{cookiecutter.package_name}}.db.metadatas import metadatas
from {{cookiecutter.package_name}}.db.reflect import reflect_database
from {{cookiecutter.package_name}}.db.sessions import sessions

DEFAULT_DB_ALIAS: str = "default"

engine: AsyncEngine = engines[DEFAULT_DB_ALIAS]
metadata: MetaData = metadatas[DEFAULT_DB_ALIAS]
session: async_sessionmaker[AsyncSession] = sessions[DEFAULT_DB_ALIAS]

__all__ = [
    "DEFAULT_DB_ALIAS",
    "engine",
    "engines",
    "metadata",
    "metadatas",
    "reflect_database",
    "session",
    "sessions",
]
