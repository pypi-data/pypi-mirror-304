from pydantic import BaseModel, Field

from .account_position import FuturesAccountPosition


class FuturesAccountPositions(BaseModel):
    """
    An object that contains information about contracts and contract positions.
    """

    contract_id: int = Field(alias="contractId")
    """Contract id"""
    contract_name: str = Field(alias="contractName")
    """The uppercase contract name, e.g., E-BTC-USDT."""
    contract_other_name: str = Field(alias="contractOtherName")
    """Currency alias"""
    contract_symbol: str = Field(alias="contractSymbol")
    """Contract currency pair"""
    positions: list[FuturesAccountPosition]
    """Position detail information"""
