from pydantic import BaseModel, Field

from odyssey_exchange_api.objects import FuturesTriggerOrder


class FuturesCurrentTriggerOrdersResponse(BaseModel):
    """
    Response of the request: :class:`odyssey_exchange_api.requests.FuturesCurrentTriggerOrdersRequest`.

    An object with count and list of trigger orders.
    """

    count: int
    """Count of available trigger orders"""
    trigger_order_list: list[FuturesTriggerOrder] = Field(alias="trigOrderList")
    """Array with trigger order objects"""
