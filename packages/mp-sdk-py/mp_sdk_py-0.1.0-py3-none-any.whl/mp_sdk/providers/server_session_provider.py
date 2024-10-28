from typing import Optional
from datetime import datetime
from ..core.credential_provider import ICredentialProvider
from ..models.credential_data import CredentialData
from ..interfaces.server_interfaces import IServerInterface
from ..models.session_data import SessionData

class ServerSessionProvider(ICredentialProvider):
    """Provider that interacts with server session"""

    def __init__(self, server: IServerInterface, session_id: str):
        self.server = server
        self.session_id = session_id

    async def get_credential(self, key: str) -> Optional[CredentialData]:
        result = await self.server.get_session_data(self.session_id, key)
        if result.is_success and result.data:
            session_data: SessionData = result.data
            return CredentialData(
                content=session_data.content,
                timestamp=session_data.timestamp
            )
        return None

    async def set_credential(self, key: str, value: str, expire_seconds: int = 180) -> bool:
        session_data = SessionData(content=value, timestamp=datetime.now())
        result = await self.server.set_session_data(self.session_id, key, session_data)
        return result.is_success