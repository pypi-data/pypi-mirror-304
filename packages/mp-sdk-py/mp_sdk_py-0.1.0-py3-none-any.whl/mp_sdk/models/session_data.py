from typing import Dict, Any, TypeVar, Optional

T = TypeVar('T')

class SessionData:
    def __init__(self):
        self._sessions: Dict[str, Any] = {}

    def get_transient_value(self, key: str, default_value: T) -> T:
        return self._sessions.get(key, default_value)

    def set_transient_value(self, key: str, value: Any):
        self._sessions[key] = value

    def clear(self):
        self._sessions.clear()