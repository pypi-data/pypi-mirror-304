# core/pay_context.py
from typing import Optional
from dataclasses import dataclass
from ..models.monitor_account import MonitorAccount
from .server_session import ServerSession
from ..interfaces.server_interfaces import IServerInterface
from ..core.credential_manager import CredentialManager

@dataclass
class PayContext:
    account: MonitorAccount = None
    callback_gateway: str = None
    session: ServerSession = None
    server: IServerInterface = None
    is_test_mode: bool = False
    _credential_manager: Optional[CredentialManager] = None

    @property
    def credential(self) -> CredentialManager:
        """Lazy initialization of credential manager"""
        if self._credential_manager is None:
            self._credential_manager = CredentialManager(
                account=self.account,
                server=self.server,
                is_test_mode=self.is_test_mode
            )
        return self._credential_manager