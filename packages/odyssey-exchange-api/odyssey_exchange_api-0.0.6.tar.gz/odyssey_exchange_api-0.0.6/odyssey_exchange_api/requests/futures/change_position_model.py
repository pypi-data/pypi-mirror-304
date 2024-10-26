from pydantic import Field

from odyssey_exchange_api.base import BASE_FUTURES_URL
from odyssey_exchange_api.enums import FuturesPositionModel
from odyssey_exchange_api.requests.base import SignedRequest, ResponseType


class FuturesChangePositionModelRequest(SignedRequest[bool]):
    """
    Change position model. Returns a :class:`bool`.
    """

    _request_url = BASE_FUTURES_URL
    _request_method = "POST"
    _request_path = "/fapi/v1/edit_user_position_model"

    __returning__ = bool

    contract_name: str = Field(serialization_alias="contractName")
    """The uppercase contract name, e.g., E-BTC-USDT."""
    position_model: FuturesPositionModel = Field(serialization_alias="positionModel")
    """The model of position."""

    def make_response(self, data) -> ResponseType:
        if data.get("code") == "0" and data.get("msg") == "成功":
            return True
        return False
