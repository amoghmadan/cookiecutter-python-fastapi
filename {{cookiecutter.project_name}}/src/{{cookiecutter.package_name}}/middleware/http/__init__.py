from collections.abc import Awaitable, Callable, Coroutine
from typing import Any

from fastapi import Request, Response

from {{cookiecutter.package_name}}.middleware.http.exception import exception_middleware

http: list[
    Callable[
        [Request, Callable[[Request], Awaitable[Response]]],
        Coroutine[Any, Any, Response],
    ]
] = [exception_middleware]

__all__ = ["http"]
