import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from typer.testing import CliRunner

os.environ.setdefault("FASTAPI_SETTINGS_MODULE", "test.settings")


@pytest.fixture
def client() -> Generator[TestClient]:
    """ASGI test client with application lifespan running."""
    from {{cookiecutter.package_name}}.asgi import application

    with TestClient(application) as test_client:
        yield test_client


@pytest.fixture
def cli_client() -> CliRunner:
    """Click/Typer runner for invoking the {{cookiecutter.package_name}} CLI."""
    return CliRunner()
