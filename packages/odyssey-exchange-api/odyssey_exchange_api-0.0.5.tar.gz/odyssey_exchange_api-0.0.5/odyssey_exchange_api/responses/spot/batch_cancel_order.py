from pydantic import BaseModel


class SpotBatchCancelOrderResponse(BaseModel):
    """
    Response of the request: :class:`odyssey_exchange_api.requests.SpotBatchCancelOrderRequest`.

    Contains an arrays with successful cancelled order ids and failed order ids.

    Cancellation failure is usually because the order does not exist or the order status has reached the final state.
    """

    success: list[int] = []
    """An array of ID orders that have been canceled"""
    failed: list[int] = []
    """An array of ID orders that could not be canceled"""
