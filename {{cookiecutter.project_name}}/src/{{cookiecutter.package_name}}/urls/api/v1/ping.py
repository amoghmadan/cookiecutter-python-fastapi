from http import HTTPMethod, HTTPStatus

from fastapi import APIRouter

from {{cookiecutter.package_name}}.views import pong

ping: APIRouter = APIRouter(prefix="/ping")
ping.add_api_route("/", pong, status_code=HTTPStatus.OK, methods=[HTTPMethod.GET])

__all__ = ["ping"]
