from dataclasses import dataclass
from typing import List

@dataclass
class UploadMonitorAccountState:
    account_id: str
    current_state: int
    last_schedule_time: int
    error_count: int
    login_state: int

@dataclass
class UploadNodeState:
    node_id: str
    account_states: List[UploadMonitorAccountState]