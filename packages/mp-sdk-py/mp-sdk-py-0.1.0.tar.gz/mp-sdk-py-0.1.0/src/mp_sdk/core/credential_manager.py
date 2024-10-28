from typing import Optional
from datetime import datetime
import asyncio
import logging
from ..models.monitor_account import MonitorAccount
from ..interfaces.server_interfaces import IServerInterface
from .credential_pool import CredentialPool
from ..providers.bullet_sms_provider import BulletSmsProvider
from ..providers.server_session_provider import ServerSessionProvider
from ..providers.console_provider import ConsoleCredentialProvider


class CredentialManager:
    """Manages credential retrieval with appropriate providers based on context"""

    def __init__(self,
                 account: MonitorAccount,
                 server: IServerInterface,
                 is_test_mode: bool = False):
        self.account = account
        self.server = server
        self.is_test_mode = is_test_mode
        self.credential_pool = CredentialPool()
        self._bullet_provider: Optional[BulletSmsProvider] = None
        self._server_provider: Optional[ServerSessionProvider] = None
        self._console_provider: Optional[ConsoleCredentialProvider] = None
        self._setup_providers()

    def _setup_providers(self):
        """Setup appropriate providers based on context"""
        if self.is_test_mode:
            # In test mode, only use console provider
            self._console_provider = ConsoleCredentialProvider()
            self.credential_pool.register_provider(self._console_provider)
        else:
            # In production mode, setup automated providers
            if self.account.bullet_api_key:  # 假设 MonitorAccount 添加了这个字段
                self._bullet_provider = BulletSmsProvider(
                    token=self.account.bullet_api_key
                )
                self.credential_pool.register_provider(self._bullet_provider)

            # Always setup server provider in production
            self._server_provider = ServerSessionProvider(
                server=self.server,
                session_id=self.account.account_id
            )
            self.credential_pool.register_provider(self._server_provider)

    async def get_next_otp(self, wait_seconds: int = 180) -> Optional[str]:
        """
        Get next available OTP. In production mode, tries both Bullet SMS and server session.
        In test mode, prompts via console.
        """
        return await self.credential_pool.get_credential("OTP", wait_seconds)

    async def get_transfer_password(self, wait_seconds: int = 180) -> Optional[str]:
        """
        Get transfer password. Similar behavior to OTP but with different key.
        """
        return await self.credential_pool.get_credential("TRANSFER_PASSWORD", wait_seconds)

    async def get_google_auth_code(self, wait_seconds: int = 180) -> Optional[str]:
        """
        Get Google Authenticator code. Similar behavior to OTP but with different key.
        """
        return await self.credential_pool.get_credential("GOOGLE_AUTH", wait_seconds)