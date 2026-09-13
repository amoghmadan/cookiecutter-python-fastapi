import asyncio
import json

from fastapi import Request
from fastapi.responses import JSONResponse

from {{cookiecutter.package_name}}.middleware.http.exception import exception_middleware


def make_request() -> Request:
    return Request({"type": "http", "asgi": {"version": "3.0"}})


def test_exception_middleware_passes_through_success_response():
    request = make_request()

    async def run():
        async def call_next(_: Request):
            return JSONResponse({"ok": True})

        return await exception_middleware(request, call_next)

    response = asyncio.run(run())
    assert json.loads(response.body) == {"ok": True}


def test_exception_middleware_returns_internal_server_error():
    request = make_request()

    async def run():
        async def call_next(_: Request):
            raise RuntimeError("boom")

        return await exception_middleware(request, call_next)

    response = asyncio.run(run())
    assert response.status_code == 500
    assert json.loads(response.body) == {"detail": "Internal Server Error"}
