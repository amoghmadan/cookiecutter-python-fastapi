from collections.abc import Awaitable, Callable, Coroutine
from typing import Any

from fastapi import Request, Response

from {{cookiecutter.package_name}}.middleware.http import http

middlewares: dict[
    str,
    list[
        Callable[
            [Request, Callable[[Request], Awaitable[Response]]],
            Coroutine[Any, Any, Response],
        ]
    ],
] = {"http": http}

__all__ = ["middlewares"]
