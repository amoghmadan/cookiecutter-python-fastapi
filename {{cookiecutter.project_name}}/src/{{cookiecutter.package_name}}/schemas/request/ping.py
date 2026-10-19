from pydantic import BaseModel


class PingRequest(BaseModel):
    """Reply: Pong"""

    throw: bool = False
