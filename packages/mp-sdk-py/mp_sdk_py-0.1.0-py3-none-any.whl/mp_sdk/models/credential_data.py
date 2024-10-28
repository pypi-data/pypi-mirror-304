from dataclasses import dataclass
from datetime import datetime

@dataclass
class CredentialData:
    """Credential data with expiration"""
    content: str
    timestamp: datetime
    expire_seconds: int = 180  # Default 3 minutes

    @property
    def is_valid(self) -> bool:
        if not self.content:
            return False
        elapsed = (datetime.now() - self.timestamp).total_seconds()
        return elapsed <= self.expire_seconds