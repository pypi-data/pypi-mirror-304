from decimal import Decimal

from pydantic import BaseModel


class WebsocketFullDepth(BaseModel):
    asks: list[list[Decimal]]
    buys: list[list[Decimal]]
