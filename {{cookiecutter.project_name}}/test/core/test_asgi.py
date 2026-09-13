import asyncio

from fastapi import FastAPI

from {{cookiecutter.package_name}}.core.asgi import get_asgi_application
from {{cookiecutter.package_name}}.db import engines, sessions
from {{cookiecutter.package_name}}.utils.lifespan import lifespan


def test_get_asgi_application_returns_fastapi_app():
    application = get_asgi_application()
    assert isinstance(application, FastAPI)


def test_lifespan_sets_engine_and_session_state():
    application = FastAPI()

    async def run():
        async with lifespan(application):
            assert application.state.engines == engines
            assert application.state.sessions == sessions

    asyncio.run(run())
