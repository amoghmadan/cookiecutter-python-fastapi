from fastapi.routing import APIRoute

from {{cookiecutter.package_name}}.urls.api.v1.ping import ping
from {{cookiecutter.package_name}}.views import pong


def test_ping_route_is_registered():
    routes = [route for route in ping.routes if isinstance(route, APIRoute)]
    assert len(routes) == 1
    route = routes[0]

    assert route.path == "/ping/"
    assert route.methods == {"GET"}
    assert route.endpoint is pong
