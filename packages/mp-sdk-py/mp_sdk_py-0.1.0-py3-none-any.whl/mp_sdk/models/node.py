from dataclasses import dataclass
from typing import List
from .monitor_account import MonitorAccount

@dataclass
class Node:
    node_id: str
    control_state: int
    monitor_accounts: List[MonitorAccount]