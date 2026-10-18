from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from {{cookiecutter.package_name}}.conf import settings
from {{cookiecutter.package_name}}.middleware import middlewares
from {{cookiecutter.package_name}}.urls import urlpatterns
from {{cookiecutter.package_name}}.utils.lifespan import lifespan


class ASGIHandler:
    """Handler for ASGI requests."""

    def __new__(cls: type) -> FastAPI:
        openapi: dict[str, Any] = {**settings.OPENAPI}
        license_info = openapi.pop("license", None)

        application: FastAPI = FastAPI(
            debug=settings.DEBUG,
            lifespan=lifespan,
            license_info=license_info,
            **openapi,
        )
        for protocol in middlewares:  # Register middlewares
            for middleware in middlewares[protocol]:
                application.middleware(protocol)(middleware)

        application.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ALLOW_ORIGINS,
            allow_methods=settings.CORS_ALLOW_METHODS,
            allow_headers=settings.CORS_ALLOW_HEADERS,
            allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        )

        for router in urlpatterns:  # Register routers
            application.include_router(router)

        return application
