from typing import Optional, Dict
import logging
from datetime import datetime, timedelta
from ..core.credential_provider import ICredentialProvider
from ..models.credential_data import CredentialData
from ..core.push_bullet_client import PushbulletClient


class BulletSmsProvider(ICredentialProvider):
    """Provider that gets OTP from Bullet SMS service via Pushbullet"""

    def __init__(self, token: str):
        self._client = PushbulletClient(token)
        self._initialized = False

    async def _ensure_initialized(self):
        """Ensure the Pushbullet client is initialized"""
        if not self._initialized:
            try:
                await self._client.init_async()
                self._initialized = True
            except Exception as e:
                logging.error(f"Failed to initialize Pushbullet client: {str(e)}")
                raise

    async def close(self):
        """Close the provider and cleanup resources"""
        if self._initialized:
            await self._client.close()
            self._initialized = False

    async def get_credential(self, key: str) -> Optional[CredentialData]:
        """Get credential by key"""
        if key != "OTP":  # Only handle OTP requests
            return None

        try:
            await self._ensure_initialized()

            # Get latest OTP from client
            if self._client.otp and self._client.otp_timestamp:
                # Check if OTP is recent enough (within last 3 minutes)
                age = datetime.now() - self._client.otp_timestamp
                if age <= timedelta(minutes=3):
                    # Create credential data and clear the OTP
                    otp = self._client.otp
                    timestamp = self._client.otp_timestamp
                    self._client.otp = None  # Clear after use
                    self._client.otp_timestamp = None

                    return CredentialData(
                        content=otp,
                        timestamp=timestamp,
                        expire_seconds=180  # 3 minutes
                    )

            return None

        except Exception as e:
            logging.error(f"Error getting credential from Bullet SMS: {str(e)}")
            return None

    async def set_credential(self, key: str, value: str, expire_seconds: int = 180) -> bool:
        """Bullet SMS provider is read-only"""
        return True