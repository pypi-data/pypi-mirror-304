from pydantic import BaseModel, Field


class FuturesCreateConditionOrderResponse(BaseModel):
    """
    Response of the request: :class:`odyssey_exchange_api.requests.FuturesCreateConditionOrderRequest`.

    Contains an arrays with trigger_ids, ids, cancel_ids.
    """

    ids: list[int]
    """Array with order ids"""
    trigger_ids: list[int] = Field(validation_alias="triggerIds")
    """Array with trigger order ids"""
    cancel_ids: list[int] = Field(validation_alias="cancelIds")
    """Array with cancelled order ids"""
