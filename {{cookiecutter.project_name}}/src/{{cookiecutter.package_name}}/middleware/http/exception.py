import logging
import logging.config
from collections.abc import Awaitable, Callable
from http import HTTPStatus

from fastapi import Request, Response
from fastapi.responses import JSONResponse

from {{cookiecutter.package_name}}.conf import settings

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger("")


async def exception_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:  # pragma: no cover
    """
    Exception Middleware
    :param request: Request, http request
    :param call_next: Callable[[Request], Awaitable[Response]], next api call
    :return: Response
    """
    response: Response = JSONResponse(
        {"detail": HTTPStatus.INTERNAL_SERVER_ERROR.phrase},
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error("API Failed", exc_info=e)
    return response
