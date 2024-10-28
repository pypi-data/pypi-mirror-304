from typing import Dict, List, Optional
from datetime import datetime
import asyncio
import logging
from ..models.credential_data import CredentialData
from ..core.credential_provider import ICredentialProvider


class CredentialPool:
    """Central credential management pool"""

    def __init__(self):
        self._providers: List[ICredentialProvider] = []
        self._local_pool: Dict[str, CredentialData] = {}

    def register_provider(self, provider: ICredentialProvider):
        """Register a credential provider"""
        self._providers.append(provider)

    def clear_providers(self):
        """Clear all registered providers"""
        self._providers.clear()

    async def get_credential(self, key: str, wait_seconds: int = 0) -> Optional[str]:
        """
        Get credential by key, optionally wait for it to become available
        """
        end_time = datetime.now().timestamp() + wait_seconds

        while True:
            # Check local pool first
            if key in self._local_pool and self._local_pool[key].is_valid:
                return self._local_pool[key].content

            # Try all providers
            for provider in self._providers:
                try:
                    cred_data = await provider.get_credential(key)
                    if cred_data and cred_data.is_valid:
                        self._local_pool[key] = cred_data
                        return cred_data.content
                except Exception as e:
                    logging.error(f"Error getting credential from provider: {str(e)}")

            # If no wait time specified or timeout reached, return None
            if wait_seconds <= 0 or datetime.now().timestamp() >= end_time:
                return None

            # Wait a bit before trying again
            await asyncio.sleep(1)

    async def set_credential(self, key: str, value: str, expire_seconds: int = 180) -> bool:
        """Set credential in local pool and notify all providers"""
        # Update local pool
        self._local_pool[key] = CredentialData(
            content=value,
            timestamp=datetime.now(),
            expire_seconds=expire_seconds
        )

        # Notify all providers
        success = True
        for provider in self._providers:
            try:
                if not await provider.set_credential(key, value, expire_seconds):
                    success = False
            except Exception as e:
                logging.error(f"Error setting credential in provider: {str(e)}")
                success = False

        return success