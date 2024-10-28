from typing import Optional
import asyncio
from ..core.credential_provider import ICredentialProvider
from ..models.credential_data import CredentialData
from datetime import datetime

class ConsoleCredentialProvider(ICredentialProvider):
    """Provider that prompts user via console"""

    async def get_credential(self, key: str) -> Optional[CredentialData]:
        print(f"\nPlease enter {key}:")
        value = input().strip()
        if value:
            return CredentialData(
                content=value,
                timestamp=datetime.now()
            )
        return None

    async def set_credential(self, key: str, value: str, expire_seconds: int = 180) -> bool:
        return True