from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from ..models.credential_data import CredentialData


class ICredentialProvider(ABC):
    """Interface for credential providers"""

    @abstractmethod
    async def get_credential(self, key: str) -> Optional[CredentialData]:
        """Get credential by key"""
        pass

    @abstractmethod
    async def set_credential(self, key: str, value: str, expire_seconds: int = 180) -> bool:
        """Set credential with expiration time"""
        pass