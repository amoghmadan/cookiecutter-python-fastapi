import asyncio
from types import SimpleNamespace
from typing import Self, cast, get_args

import pytest
from fastapi import Request
from fastapi.params import Depends

from {{cookiecutter.package_name}}.db import DEFAULT_DB_ALIAS
from {{cookiecutter.package_name}}.dependencies import DBSes
from {{cookiecutter.package_name}}.dependencies.database import GetDB


class FakeSession:
    """Async-context-manager stand-in for a database session."""

    def __init__(self) -> None:
        self.closed = False

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self.closed = True


def make_request(sessions: dict) -> Request:
    return Request(
        {
            "type": "http",
            "asgi": {"version": "3.0"},
            "app": SimpleNamespace(state=SimpleNamespace(sessions=sessions)),
        }
    )


def test_getdb_defaults_to_default_alias():
    assert GetDB().alias == DEFAULT_DB_ALIAS


def test_getdb_uses_given_alias():
    assert GetDB(alias="other").alias == "other"


def test_getdb_yields_session_from_alias_and_closes_it():
    request = make_request({DEFAULT_DB_ALIAS: FakeSession})

    async def run():
        seen = []
        async for session in GetDB()(request):
            fake = cast(FakeSession, session)
            seen.append((fake, fake.closed))
        return seen

    seen = asyncio.run(run())

    session, closed_while_open = seen[0]
    assert isinstance(session, FakeSession)
    assert closed_while_open is False
    assert session.closed is True


def test_getdb_raises_for_missing_alias():
    request = make_request({})

    async def run():
        async for _ in GetDB(alias="missing")(request):  # pragma: no cover
            pass

    with pytest.raises(KeyError, match="missing"):
        asyncio.run(run())


def test_dbses_is_annotated_with_getdb_dependency():
    _, metadata = get_args(DBSes)
    assert isinstance(metadata, Depends)
    assert isinstance(metadata.dependency, GetDB)
    assert metadata.dependency.alias == DEFAULT_DB_ALIAS
