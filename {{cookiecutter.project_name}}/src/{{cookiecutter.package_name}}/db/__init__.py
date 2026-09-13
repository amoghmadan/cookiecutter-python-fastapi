from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from {{cookiecutter.package_name}}.db.engines import engines
from {{cookiecutter.package_name}}.db.sessions import sessions

DEFAULT_DB_ALIAS: str = "default"

engine: AsyncEngine = engines[DEFAULT_DB_ALIAS]
metadata: MetaData = MetaData()
session: async_sessionmaker[AsyncSession] = sessions[DEFAULT_DB_ALIAS]

__all__ = ["DEFAULT_DB_ALIAS", "engine", "engines", "metadata", "session", "sessions"]
