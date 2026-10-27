from fastapi import APIRouter

from {{cookiecutter.package_name}}.urls.api.v1.ping import ping

urlpatterns: list[APIRouter] = [ping]

v1: APIRouter = APIRouter(prefix="/v1")
for router in urlpatterns:
    v1.include_router(router)

__all__ = ["v1"]
