from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from {{cookiecutter.package_name}}.db.engines import engines

sessions: dict[str, async_sessionmaker[AsyncSession]] = {
    alias: async_sessionmaker(engine, expire_on_commit=False, autocommit=False)
    for alias, engine in engines.items()
}
