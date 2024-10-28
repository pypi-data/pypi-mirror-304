from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

@dataclass
class QueryResult(Generic[T]):
    data: Optional[T]
    is_success: bool
    error_message: Optional[str] = None

    @classmethod
    def success(cls, data: T) -> 'QueryResult[T]':
        """Create a successful query result."""
        return cls(data=data, is_success=True)

    @classmethod
    def failure(cls, error_message: str) -> 'QueryResult[T]':
        """Create a failed query result."""
        return cls(data=None, is_success=False, error_message=error_message)

    def __bool__(self) -> bool:
        """Allow using the result in boolean contexts to check success."""
        return self.is_success