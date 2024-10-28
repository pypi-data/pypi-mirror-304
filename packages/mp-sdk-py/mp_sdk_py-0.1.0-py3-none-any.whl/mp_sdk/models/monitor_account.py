from dataclasses import dataclass
from typing import Optional

@dataclass
class MonitorAccount:
    account_id: str
    resource_id: int
    product_id: int
    required_state: int
    bank_template: str
    login_id1: str
    login_id2: str
    phone_number: str
    password: str
    transfer_password: str
    reserved0: Optional[str] = None
    reserved1: Optional[str] = None
    reserved2: Optional[str] = None
    reserved3: Optional[str] = None
    bullet_api_key: Optional[str] = None