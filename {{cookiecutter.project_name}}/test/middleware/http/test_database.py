import asyncio
from types import SimpleNamespace
from typing import Self

from fastapi import Request
from fastapi.responses import JSONResponse

from {{cookiecutter.package_name}}.db import DEFAULT_DB_ALIAS
from {{cookiecutter.package_name}}.middleware.http.database import database_middleware


class FakeSession:
    """Async-context-manager stand-in for a database session."""

    def __init__(self) -> None:
        self.closed = False

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        self.closed = True


def test_database_middleware_sets_and_closes_session():
    request = Request(
        {
            "type": "http",
            "asgi": {"version": "3.0"},
            "app": SimpleNamespace(
                state=SimpleNamespace(sessions={DEFAULT_DB_ALIAS: FakeSession})
            ),
        }
    )

    async def run():
        seen = {}

        async def call_next(current: Request):
            seen["db"] = current.state.db
            return JSONResponse({"ok": True})

        response = await database_middleware(request, call_next)
        return response, seen, request.state.db

    response, seen, db_after = asyncio.run(run())

    assert response.status_code == 200
    assert isinstance(seen["db"], FakeSession)
    assert seen["db"].closed is True
    assert db_after is seen["db"]
