from fastapi import APIRouter

from {{cookiecutter.package_name}}.urls.api import api

urlpatterns: list[APIRouter] = [api]

__all__ = ["urlpatterns"]
