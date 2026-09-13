from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession


def get_db(request: Request) -> AsyncSession:
    """
    Use "fastapi.Depends" class and pass this function to access DB object.
    :param request: Request
    :return: AsyncSession
    """
    return request.state.db


DBSes: AsyncSession = Depends(get_db)
