import asyncio
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock

import pytest

from {{cookiecutter.package_name}}.__version__ import __version__
from {{cookiecutter.package_name}}.core.exceptions import Error
from {{cookiecutter.package_name}}.schemas.request import PingRequest
from {{cookiecutter.package_name}}.schemas.response import PingResponse
from {{cookiecutter.package_name}}.views import pong


def test_pong_view_with_mock_db():
    """pong executes a query against the db and wraps the result in PingResponse."""
    db = AsyncMock()
    result = MagicMock()
    result.scalar_one.return_value = "Pong"
    db.execute.return_value = result

    response = asyncio.run(pong(PingRequest(), db))

    assert response == PingResponse(reply="Pong")
    db.execute.assert_awaited_once()
    result.scalar_one.assert_called_once_with()


def test_pong_view_raises_on_throw_flag():
    db = AsyncMock()

    with pytest.raises(Error, match="Raising custom exception for testing."):
        asyncio.run(pong(PingRequest(throw=True), db))

    db.execute.assert_not_awaited()


def test_ping_endpoint_returns_version(client):
    response = client.get("/api/v1/ping/")

    assert response.status_code == 200
    assert response.json() == {"reply": __version__}


def test_ping_endpoint_throw_returns_internal_server_error(client):
    response = client.get("/api/v1/ping/", params={"throw": "true"})

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Internal Server Error"}


def test_ping_endpoint_rejects_post(client):
    response = client.post("/api/v1/ping/")

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
