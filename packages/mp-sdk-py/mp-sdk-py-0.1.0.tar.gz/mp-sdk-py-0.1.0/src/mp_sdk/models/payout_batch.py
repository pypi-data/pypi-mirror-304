from dataclasses import dataclass
from .enums import PayoutBatchState

@dataclass
class PayoutBatch:
    id: int
    file_name: str
    order_list: str
    error_order_list: str
    state: PayoutBatchState