from abc import ABC, abstractmethod
from typing import List, Optional
from ..models.pay_context import PayContext
from ..models.action_result import ActionResult, ActionResultT
from ..models.parsed_transaction import ParsedTransaction
from ..models.payout_batch import PayoutBatch
from datetime import datetime

class IPayFunction(ABC):
    @abstractmethod
    async def initialize(self, context: PayContext):
        pass

    @abstractmethod
    async def is_login_state_valid(self, context: PayContext) -> bool:
        pass

    @abstractmethod
    async def is_webpage_session_alive(self, context: PayContext) -> bool:
        pass

    @abstractmethod
    async def support_lookup_transactions(self, context: PayContext) -> bool:
        pass

    @abstractmethod
    async def before_login(self, context: PayContext) -> ActionResult:
        pass

    @abstractmethod
    async def after_login(self, context: PayContext) -> ActionResult:
        pass

    @abstractmethod
    async def login(self, context: PayContext) -> ActionResult:
        pass

    @abstractmethod
    async def lookup_transactions(self, context: PayContext) -> ActionResultT[List[ParsedTransaction]]:
        pass

    @abstractmethod
    async def support_payout(self, context: PayContext) -> bool:
        pass

    @abstractmethod
    async def payout_new_batches(self, context: PayContext, batches: List[PayoutBatch]) -> ActionResult:
        pass

    @abstractmethod
    async def payout_check_batches_state(self, context: PayContext, batches: List[PayoutBatch]) -> ActionResult:
        pass

    @abstractmethod
    async def support_query_balance(self, context: PayContext) -> bool:
        pass

    @abstractmethod
    async def query_balance(self, context: PayContext) -> ActionResultT[int]:
        pass

    @abstractmethod
    async def support_test_card(self, context: PayContext) -> bool:
        pass

    @abstractmethod
    async def test_card(self, context: PayContext) -> ActionResult:
        pass

    @abstractmethod
    async def payout_new_batches(self, context: PayContext, batches: List[PayoutBatch]) -> ActionResult:
        pass

    @abstractmethod
    async def payout_check_batches_state(self, context: PayContext, batches: List[PayoutBatch]) -> ActionResult:
        pass

class PayFunctionBase(IPayFunction):
    async def initialize(self, context: PayContext):
        await self.do_initialize(context)

    async def do_initialize(self, context: PayContext):
        pass

    async def is_webpage_session_alive(self, context: PayContext) -> bool:
        return await self.do_is_webpage_session_alive(context)

    async def do_is_webpage_session_alive(self, context: PayContext) -> bool:
        return False

    async def is_login_state_valid(self, context: PayContext) -> bool:
        return await self.do_is_login_state_valid(context)

    async def do_is_login_state_valid(self, context: PayContext) -> bool:
        last_login_timestamp = context.session.get_value[Optional[datetime]]("lastLoginTimestamp")
        return last_login_timestamp is not None

    async def support_lookup_transactions(self, context: PayContext) -> bool:
        return True

    async def before_login(self, context: PayContext) -> ActionResult:
        return await self.do_before_login(context)

    async def do_before_login(self, context: PayContext) -> ActionResult:
        return ActionResult.success_result()

    async def after_login(self, context: PayContext) -> ActionResult:
        return await self.do_after_login(context)

    async def do_after_login(self, context: PayContext) -> ActionResult:
        return ActionResult.success_result()

    @abstractmethod
    async def do_login(self, context: PayContext) -> ActionResult:
        pass

    async def login(self, context: PayContext) -> ActionResult:
        return await self.do_login(context)

    @abstractmethod
    async def do_lookup_transactions(self, context: PayContext) -> ActionResultT[List[ParsedTransaction]]:
        pass

    async def lookup_transactions(self, context: PayContext) -> ActionResultT[List[ParsedTransaction]]:
        return await self.do_lookup_transactions(context)

    async def support_query_balance(self, context: PayContext) -> bool:
        return False

    async def support_test_card(self, context: PayContext) -> bool:
        return False

    async def payout_new_batches(self, context: PayContext, batches: List[PayoutBatch]) -> ActionResult:
        return await self.do_payout_new_batches(context, batches)

    async def do_payout_new_batches(self, context: PayContext, batches: List[PayoutBatch]) -> ActionResult:
        pass

    async def payout_check_batches_state(self, context: PayContext, batches: List[PayoutBatch]) -> ActionResult:
        return await self.do_payout_check_batches_state(context, batches);

    async def do_payout_check_batches_state(self, context: PayContext, batches: List[PayoutBatch]) -> ActionResult:
        pass