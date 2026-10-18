from types import AsyncGeneratorType
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from {{cookiecutter.package_name}}.db import DEFAULT_DB_ALIAS


class GetDB:
    """Get: DB"""

    def __init__(self, alias: str = DEFAULT_DB_ALIAS) -> None:
        self.alias = alias

    async def __call__(
        self, request: Request
    ) -> AsyncGeneratorType[AsyncSession, None]:
        """
        Use "fastapi.Depends" class and pass this function to access DB object.
        :param request: Request
        :return: AsyncSession
        """
        session_class: async_sessionmaker[AsyncSession] = request.app.state.sessions[
            self.alias
        ]
        async with session_class() as session:
            yield session


DBSes = Annotated[AsyncSession, Depends(GetDB())]
