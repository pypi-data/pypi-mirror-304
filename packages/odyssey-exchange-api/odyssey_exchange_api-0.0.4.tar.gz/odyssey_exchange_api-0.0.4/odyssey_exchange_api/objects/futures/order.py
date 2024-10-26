from decimal import Decimal

from pydantic import BaseModel, Field

from odyssey_exchange_api.enums import FuturesOrderStatus, FuturesOrderType, FuturesOrderSide


class FuturesOrder(BaseModel):
    """
    An object that contains information about the order.
    """

    order_id: int = Field(alias="orderId")
    """Order ID"""
    contract_name: str = Field(alias="contractName")
    """The uppercase contract name, e.g., E-BTC-USDT."""
    transact_time: int | None = Field(default=None, alias="transactTime")
    """The time of place order"""
    price: Decimal
    """Order price"""
    original_quantity: Decimal = Field(alias="origQty")
    """Order volume"""
    executed_quantity: Decimal = Field(alias="executedQty")
    """The number of already deal order"""
    average_price: Decimal | None = Field(alias="avgPrice")
    """The average price of already deal order"""
    type: FuturesOrderType
    """Type of the order"""
    side: FuturesOrderSide
    """Side of the order"""
    status: FuturesOrderStatus
    """Order status"""
    time_in_force: str | int = Field(alias="timeInForce")
    """Effective method of conditional order"""
