from {{cookiecutter.package_name}}.schemas.base import Schema


class PingRequest(Schema):
    """Reply: Pong"""

    throw: bool = False


class PingResponse(Schema):
    """Reply: Pong"""

    reply: str
