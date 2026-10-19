from pydantic import BaseModel


class PingResponse(BaseModel):
    """Reply: Pong"""

    reply: str
