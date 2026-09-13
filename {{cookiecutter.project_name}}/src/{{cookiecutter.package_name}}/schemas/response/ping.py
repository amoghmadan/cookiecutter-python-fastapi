from pydantic import BaseModel


class Pong(BaseModel):
    """Reply: Pong"""

    reply: str
