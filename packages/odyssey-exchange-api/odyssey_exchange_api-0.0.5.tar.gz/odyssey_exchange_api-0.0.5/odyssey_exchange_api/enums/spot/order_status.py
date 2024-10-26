from enum import Enum


# TODO: check enum values
class SpotOrderStatus(str, Enum):
    NEW = "NEW"
    NEW_ORDER = "New Order"

    PARTIALLY_FILLED = "Partially Filled"
    FILLED = "Filled"
    CANCELLED = "Cancelled"
    TO_BE_CANCELLED = "PENDING_CANCEL"
    PARTIALLY_FILLED_OR_CANCELLED = "Partially Filled/Cancelled"
    REJECTED = "REJECTED"
