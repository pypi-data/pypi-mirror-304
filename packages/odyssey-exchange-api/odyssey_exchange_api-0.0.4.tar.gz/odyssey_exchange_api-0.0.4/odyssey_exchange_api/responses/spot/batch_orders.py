from pydantic import BaseModel


class SpotBatchOrdersResponse(BaseModel):
    """
    Response of the request: :class:`odyssey_exchange_api.requests.SpotBatchOrdersRequest`.

    Contains an array of created order_ids.
    """

    ids: list[str]
    """Array of created order ids"""
