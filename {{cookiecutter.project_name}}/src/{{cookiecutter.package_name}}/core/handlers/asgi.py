from fastapi import FastAPI

from {{cookiecutter.package_name}}.conf import settings
from {{cookiecutter.package_name}}.middleware import middlewares
from {{cookiecutter.package_name}}.urls import urlpatterns
from {{cookiecutter.package_name}}.utils.lifespan import lifespan


class ASGIHandler:
    """Handler for ASGI requests."""

    def __new__(cls: type) -> FastAPI:
        application: FastAPI = FastAPI(
            debug=settings.DEBUG,
            lifespan=lifespan,
            **settings.OPENAPI,
        )

        for protocol in middlewares:  # Register middlewares
            for middleware in middlewares[protocol]:
                application.middleware(protocol)(middleware)

        for router in urlpatterns:  # Register routers
            application.include_router(router)

        return application
