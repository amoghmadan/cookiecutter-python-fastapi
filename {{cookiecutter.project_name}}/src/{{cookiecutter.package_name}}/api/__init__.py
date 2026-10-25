from fastapi import APIRouter

from {{cookiecutter.package_name}}.api.v1 import v1

urlpatterns: list[APIRouter] = [v1]

api: APIRouter = APIRouter(prefix="/api")
for router in urlpatterns:
    api.include_router(router)

__all__ = ["api"]
