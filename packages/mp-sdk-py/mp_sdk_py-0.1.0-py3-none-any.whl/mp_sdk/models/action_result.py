from dataclasses import dataclass
from typing import Generic, TypeVar, Optional
from .enums import ResultType

T = TypeVar('T')

@dataclass
class ActionResult:
    state: ResultType = ResultType.Success
    error_message: str = ""

    @property
    def success(self) -> bool:
        return self.state == ResultType.Success

    @property
    def error(self) -> bool:
        return self.state == ResultType.Error

    @classmethod
    def success_result(cls) -> 'ActionResult':
        return cls(state=ResultType.Success)

    def fail(self, error: str) -> 'ActionResult':
        return ActionResult(
            state=ResultType.Error,
            error_message=error
        )

@dataclass
class ActionResultT(ActionResult, Generic[T]):
    result: Optional[T] = None

    @classmethod
    def ok(cls, data: T) -> 'ActionResultT[T]':
        return cls(
            state=ResultType.Success,
            result=data
        )