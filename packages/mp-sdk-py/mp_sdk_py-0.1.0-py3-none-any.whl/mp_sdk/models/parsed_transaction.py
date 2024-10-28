from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ParsedTransaction:
    time: Optional[datetime]
    amount: float
    balance: float
    detail: str
    transaction_code: str
    transaction_type: int
    target_card_number: str
    message_identify_code: str
    name: str