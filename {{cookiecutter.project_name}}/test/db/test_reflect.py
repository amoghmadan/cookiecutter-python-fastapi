import asyncio
from collections.abc import Mapping
from types import SimpleNamespace, TracebackType
from typing import Any, cast

import pytest
from sqlalchemy import MetaData, Table, text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from {{cookiecutter.package_name}}.db import reflect
from {{cookiecutter.package_name}}.db.reflect import reflect_database


class FakeConnection:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def run_sync(self, _fn: Any, **kwargs: Any) -> None:
        self.calls.append(kwargs)


class FakeBegin:
    def __init__(self, connection: FakeConnection) -> None:
        self.connection = connection

    async def __aenter__(self) -> FakeConnection:
        return self.connection

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        return None


class FakeEngine:
    def __init__(self, connection: FakeConnection) -> None:
        self.dialect = SimpleNamespace(name="postgresql")
        self.connection = connection

    def begin(self) -> FakeBegin:
        return FakeBegin(self.connection)


def test_reflect_database_returns_cached_tables_without_reflection():
    tables = asyncio.run(reflect_database("default"))

    assert tables is reflect.metadatas["default"].tables


def test_reflect_database_reflects_sqlite_tables(tmp_path, monkeypatch):
    async def scenario() -> Mapping[str, Table]:
        engine: AsyncEngine = create_async_engine(
            f"sqlite+aiosqlite:///{tmp_path / 'reflect.sqlite3'}"
        )
        async with engine.begin() as connection:
            await connection.execute(
                text("CREATE TABLE article (id INTEGER PRIMARY KEY)")
            )
        monkeypatch.setitem(reflect.engines, "sqlite-reflect", engine)
        monkeypatch.setitem(reflect.metadatas, "sqlite-reflect", MetaData())
        try:
            return await reflect_database("sqlite-reflect", main=["article"])
        finally:
            await engine.dispose()

    tables = asyncio.run(scenario())

    assert set(tables) == {"article"}
    assert "article" in reflect.metadatas["sqlite-reflect"].tables


def test_reflect_database_passes_schema_for_non_sqlite(monkeypatch):
    connection = FakeConnection()
    engine = cast(AsyncEngine, FakeEngine(connection))
    monkeypatch.setitem(reflect.engines, "postgres-reflect", engine)
    monkeypatch.setitem(reflect.metadatas, "postgres-reflect", MetaData())

    asyncio.run(reflect_database("postgres-reflect", analytics=["article"]))

    assert connection.calls == [{"only": ["article"], "schema": "analytics"}]


def test_reflect_database_reflects_all_tables_for_empty_list(monkeypatch):
    connection = FakeConnection()
    engine = cast(AsyncEngine, FakeEngine(connection))
    monkeypatch.setitem(reflect.engines, "postgres-reflect-all", engine)
    monkeypatch.setitem(reflect.metadatas, "postgres-reflect-all", MetaData())

    asyncio.run(reflect_database("postgres-reflect-all", analytics=[]))

    assert connection.calls == [{"only": None, "schema": "analytics"}]


def test_reflect_database_rejects_unknown_alias():
    with pytest.raises(KeyError):
        asyncio.run(reflect_database("missing"))
