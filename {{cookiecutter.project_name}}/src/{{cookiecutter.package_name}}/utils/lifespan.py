from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from {{cookiecutter.package_name}}.db import engines, sessions


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator:
    """
    Lifespan for FastAPI application.
    :param application: FastAPI
    :return: AsyncGenerator
    """
    application.state.engines = engines
    application.state.sessions = sessions
    yield
