import asyncio
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock

from {{cookiecutter.package_name}}.schemas.response import Pong
from {{cookiecutter.package_name}}.views import pong


def test_pong_view_with_mock_db():
    """pong executes a query against the db and wraps the result in Pong."""
    db = AsyncMock()
    result = MagicMock()
    result.scalar_one.return_value = "Pong"
    db.execute.return_value = result

    response = asyncio.run(pong(db))

    assert response == Pong(reply="Pong")
    db.execute.assert_awaited_once()
    result.scalar_one.assert_called_once_with()


def test_ping_endpoint_returns_pong(client):
    response = client.get("/api/v1/ping/")

    assert response.status_code == 200
    assert response.json() == {"reply": "Pong"}


def test_ping_endpoint_rejects_post(client):
    response = client.post("/api/v1/ping/")

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
