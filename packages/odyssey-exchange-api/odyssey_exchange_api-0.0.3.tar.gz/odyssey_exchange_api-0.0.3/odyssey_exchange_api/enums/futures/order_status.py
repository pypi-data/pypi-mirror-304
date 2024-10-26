from enum import Enum


class FuturesOrderStatus(str, Enum):
    INIT = "INIT"

    NEW = "NEW"
    NEW_ORDER = "New Order"

    PARTIALLY_FILLED = "PART_FILLED"
    FILLED = "FILLED"
    CANCELLED = "Cancelled"
    TO_BE_CANCELLED = "PENDING_CANCEL"
    PARTIALLY_FILLED_OR_CANCELLED = "Partially Filled/Cancelled"
    REJECTED = "REJECTED"
