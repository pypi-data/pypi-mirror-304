# core/server_session.py
from typing import Dict, Optional, TypeVar, Any
from datetime import datetime
from playwright.async_api import Page, Browser, Playwright
from .session_data import SessionData
from .session_keys import SessionKeys

T = TypeVar('T')

class ServerSession:
    def __init__(self):
        self._session_datas: Dict[str, SessionData] = {}

    @property
    def page(self) -> Optional[Page]:
        return self.get_value("AutomationMainPage", None, SessionKeys.RuntimeObject)

    @page.setter
    def page(self, value: Page):
        self.set_value("AutomationMainPage", value, SessionKeys.RuntimeObject)

    @property
    def browser(self) -> Optional[Browser]:
        return self.get_value("AutomationBrowser", None, SessionKeys.RuntimeObject)

    @browser.setter
    def browser(self, value: Browser):
        self.set_value("AutomationBrowser", value, SessionKeys.RuntimeObject)

    @property
    def driver(self) -> Optional[Playwright]:
        return self.get_value("AutomationDriver", None, SessionKeys.RuntimeObject)

    @driver.setter
    def driver(self, value: Playwright):
        self.set_value("AutomationDriver", value, SessionKeys.RuntimeObject)

    @property
    def lookup_transactions_data(self) -> Optional[str]:
        return self.get_value("TransactionData", None, SessionKeys.SessionObject)

    @lookup_transactions_data.setter
    def lookup_transactions_data(self, value: str):
        self.set_value("TransactionData", value, SessionKeys.SessionObject)

    @property
    def last_user_click_time(self) -> Optional[datetime]:
        return self.get_value("LastUserClickTime")

    @last_user_click_time.setter
    def last_user_click_time(self, value: Optional[datetime]):
        self.set_value("LastUserClickTime", value)

    def get_session_value(self, key: str, default_value: T = None) -> T:
        return self.get_value(key, default_value, SessionKeys.SessionObject)

    def get_value(self, key: str, default_value: T = None, flag: str = SessionKeys.SessionObject) -> T:
        if flag in self._session_datas:
            return self._session_datas[flag].get_transient_value(key, default_value)
        return default_value

    def get_int_value(self, key: str, default_value: int = 0) -> int:
        return self.get_value(key, default_value)

    def set_value(self, key: str, value: Any, flag: str = SessionKeys.SessionObject):
        if flag not in self._session_datas:
            self._session_datas[flag] = SessionData()
        self._session_datas[flag].set_transient_value(key, value)

    def clear(self, flag: str = SessionKeys.SessionObject):
        if flag in self._session_datas:
            self._session_datas[flag].clear()