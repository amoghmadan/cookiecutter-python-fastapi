from collections.abc import Mapping

from sqlalchemy import Table

from {{cookiecutter.package_name}}.db.engines import engines
from {{cookiecutter.package_name}}.db.metadatas import metadatas


async def reflect_database(alias: str, **target_tables: list[str]) -> Mapping[str, Table]:
    """
    Asynchronously reflects tables from a specified database engine into a cached MetaData instance.

    :param alias: str
    :param target_tables: list[str]
    :return: Mapping[str, Table]
    """
    metadata = metadatas[alias]
    if not target_tables:
        return metadata.tables
    engine = engines[alias]
    async with engine.begin() as conn:
        for schema, tables in target_tables.items():
            if engine.dialect.name == "sqlite":
                await conn.run_sync(metadata.reflect, only=tables or None)
            else:
                await conn.run_sync(
                    metadata.reflect,
                    only=tables or None,
                    schema=schema,
                )
    return metadata.tables
