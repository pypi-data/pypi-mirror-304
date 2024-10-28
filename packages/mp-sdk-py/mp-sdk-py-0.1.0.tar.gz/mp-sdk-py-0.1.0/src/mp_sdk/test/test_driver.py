from __future__ import annotations
from typing import TypeVar, Generic, Type, Optional, List

from mp_sdk.src.mp_sdk.interfaces.pay_function import IPayFunction
from mp_sdk.src.mp_sdk.models.monitor_account import MonitorAccount
from mp_sdk.src.mp_sdk.models.pay_context import PayContext
from mp_sdk.src.mp_sdk.models.parsed_transaction import ParsedTransaction
from mp_sdk.src.mp_sdk.models.payout_batch import PayoutBatch
from mp_sdk.src.mp_sdk.models.server_session import ServerSession
from mp_sdk.src.mp_sdk.models.action_result import ActionResult, ActionResultT
from mp_sdk.src.mp_sdk.test.mock_server import MockServerInterface

T = TypeVar('T', bound=IPayFunction)


class TestDriver(Generic[T]):
    """Test driver for PayFunction implementations"""

    def __init__(self,
                 function_type: Type[T],
                 account: MonitorAccount,
                 payout_file_path: Optional[str] = None):
        self.function_type = function_type
        self.account = account
        self.server_interface = MockServerInterface(payout_file_path)
        self.pay_function: Optional[T] = None
        self.context: Optional[PayContext] = None
        self._cleanup_required = False

    async def _ensure_initialized(self):
        """Ensures the pay function and context are initialized"""
        if self.pay_function is None:
            self.pay_function = self.function_type()

            # Create PayContext with appropriate test mode setting
            is_test_mode = not bool(self.account.bullet_api_key)
            self.context = PayContext(
                account=self.account,
                callback_gateway="test_gateway",
                session=ServerSession(),
                server=self.server_interface,
                is_test_mode=is_test_mode
            )

            self._cleanup_required = True
            await self.pay_function.initialize(self.context)

    async def cleanup(self):
        """Cleanup resources"""
        if self._cleanup_required and self.context:
            await self.context.credential.cleanup()
            self._cleanup_required = False

    async def get_next_otp(self, wait_seconds: int = 180) -> Optional[str]:
        """Helper method to get next OTP"""
        await self._ensure_initialized()
        return await self.context.credential.get_next_otp(wait_seconds)

    async def get_transfer_password(self, wait_seconds: int = 180) -> Optional[str]:
        """Helper method to get transfer password"""
        await self._ensure_initialized()
        return await self.context.credential.get_transfer_password(wait_seconds)

    async def login(self) -> ActionResult:
        """Execute the login flow"""
        await self._ensure_initialized()

        try:
            before_result = await self.pay_function.before_login(self.context)
            if not before_result.success:
                return before_result

            login_result = await self.pay_function.login(self.context)
            if not login_result.success:
                return login_result

            return await self.pay_function.after_login(self.context)
        except Exception as e:
            return ActionResult().fail(f"Login failed: {str(e)}")

    async def lookup_transactions(self) -> ActionResultT[List[ParsedTransaction]]:
        """Execute the transaction lookup flow"""
        await self._ensure_initialized()

        try:
            login_result = await self.login()
            if not login_result.success:
                return ActionResultT[List[ParsedTransaction]](
                    state=login_result.state,
                    error_message=login_result.error_message
                )

            return await self.pay_function.lookup_transactions(self.context)
        except Exception as e:
            return ActionResultT[List[ParsedTransaction]]().fail(f"Lookup transactions failed: {str(e)}")

    async def execute_payout(self) -> ActionResult:
        """Execute the complete payout flow including status check"""
        await self._ensure_initialized()

        try:
            # Ensure logged in
            login_result = await self.login()
            if not login_result.success:
                return login_result

            # Get new batches
            batches_result = self.server_interface.get_new_payout_batches(self.account)
            if not batches_result.is_success or not batches_result.data:
                return ActionResult().fail("No payout batches available")

            # Execute payout for new batches
            payout_result = await self.pay_function.payout_new_batches(self.context, batches_result.data)
            if not payout_result.success:
                return payout_result

            # Check payout status
            check_result = await self.pay_function.payout_check_batches_state(self.context, batches_result.data)
            return check_result
        except Exception as e:
            return ActionResult().fail(f"Execute payout failed: {str(e)}")

    async def query_balance(self) -> ActionResultT[int]:
        """Execute the balance query flow"""
        await self._ensure_initialized()

        try:
            login_result = await self.login()
            if not login_result.success:
                return ActionResultT[int](
                    state=login_result.state,
                    error_message=login_result.error_message
                )

            return await self.pay_function.query_balance(self.context)
        except Exception as e:
            return ActionResultT[int]().fail(f"Query balance failed: {str(e)}")

    @property
    def uploaded_transactions(self) -> List[ParsedTransaction]:
        """Get list of transactions that were uploaded"""
        return self.server_interface.uploaded_transactions

    @property
    def payout_batches(self) -> List[PayoutBatch]:
        """Get list of all payout batches and their current states"""
        return list(self.server_interface.payout_batches.values())


class TestDriverBuilder(Generic[T]):
    """Builder for configuring and creating TestDriver instances"""

    def __init__(self, function_type: Type[T]):
        self.function_type = function_type
        self.account: Optional[MonitorAccount] = None
        self.payout_file_path: Optional[str] = None
        self.bullet_token: Optional[str] = None
        self.use_bullet_sms: bool = False

    def monitor_account(self,
                        login_id1: str,
                        password: str,
                        login_id2: str = "",
                        phone_number: str = "",
                        transfer_password: str = "") -> TestDriverBuilder[T]:
        """Configure the monitor account"""
        self.account = MonitorAccount(
            account_id="test_account",
            resource_id=1,
            product_id=1,
            required_state=1,
            bank_template="test_bank",
            login_id1=login_id1,
            login_id2=login_id2,
            phone_number=phone_number,
            password=password,
            transfer_password=transfer_password,
            bullet_api_key=None,  # Will be set by with_bullet_sms if needed
            reserved0="",
            reserved1="",
            reserved2="",
            reserved3=""
        )
        return self

    def payout_path(self, file_path: str) -> TestDriverBuilder[T]:
        """Configure the payout file path"""
        self.payout_file_path = file_path
        return self

    def with_bullet_sms(self, token: str) -> TestDriverBuilder[T]:
        """Configure Bullet SMS for OTP retrieval"""
        self.bullet_token = token
        self.use_bullet_sms = True
        return self

    def use_otp_console_input(self) -> TestDriverBuilder[T]:
        """Configure to use console input for credentials"""
        self.use_bullet_sms = False
        self.bullet_token = None
        return self

    def build(self) -> TestDriver[T]:
        """Build the TestDriver instance"""
        if self.account is None:
            raise ValueError("Monitor account must be configured")

        if self.use_bullet_sms and self.bullet_token:
            self.account.bullet_token = self.bullet_token

        return TestDriver(
            function_type=self.function_type,
            account=self.account,
            payout_file_path=self.payout_file_path
        )


def create_test_driver(function_type: Type[T]) -> TestDriverBuilder[T]:
    """Create a new TestDriverBuilder for the given PayFunction type"""
    return TestDriverBuilder(function_type)