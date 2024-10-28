import json
import re
import asyncio
import websockets
from typing import Optional
from dataclasses import dataclass


@dataclass
class PushbulletClient:
    """Client for interacting with Pushbullet websocket API"""

    def __init__(self, token: str):
        self._token = token
        self._otp_pattern = r'\b\d{6,}\b'
        self.otp: Optional[str] = None
        self.web_socket = None
        self.card_no: Optional[str] = None
        self.identify_code: Optional[str] = None
        self._running = False
        self._receive_task: Optional[asyncio.Task] = None

    async def init_async(self):
        """Initialize the websocket connection and start message processing"""
        server_url = f"wss://stream.pushbullet.com/websocket/{self._token}"
        self.web_socket = await websockets.connect(server_url)
        self._running = True
        self._receive_task = asyncio.create_task(self._receive_messages())

    async def close(self):
        """Close the websocket connection and cleanup"""
        self._running = False
        if self.web_socket:
            await self.web_socket.close()
        if self._receive_task:
            await self._receive_task

    async def _receive_messages(self):
        """Background task to receive and process messages"""
        try:
            while self._running and self.web_socket:
                try:
                    message = await self.web_socket.recv()
                    try:
                        message_data = json.loads(message)
                        if "push" in message_data:
                            push_data = message_data["push"]
                            if (push_data.get("notifications") and
                                    push_data.get("type") == "sms_changed"):

                                for notification in push_data["notifications"]:
                                    sms_content = notification.get("body", "")
                                    match = re.search(self._otp_pattern, sms_content)
                                    if match:
                                        self.otp = match.group(0)

                    except json.JSONDecodeError:
                        pass  # Ignore invalid JSON
                    except Exception as ex:
                        print(f"Error processing message: {str(ex)}")

                except websockets.exceptions.ConnectionClosed:
                    print("WebSocket connection closed")
                    break
                except Exception as ex:
                    print(f"Error receiving message: {str(ex)}")

        finally:
            self._running = False
            if self.web_socket:
                await self.web_socket.close()
            print("Disconnected from server.")