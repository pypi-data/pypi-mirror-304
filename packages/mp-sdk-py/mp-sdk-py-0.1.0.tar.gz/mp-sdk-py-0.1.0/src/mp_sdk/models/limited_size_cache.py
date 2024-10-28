from collections import deque
from typing import Generic, TypeVar, Set

T = TypeVar('T')


class LimitedSizeCache(Generic[T]):
    def __init__(self, max_size: int):
        if max_size <= 0:
            raise ValueError("MaxSize must be greater than 0")

        self._max_size = max_size
        self._queue: deque[T] = deque(maxlen=max_size)
        self._set: Set[T] = set()

    def add(self, item: T) -> bool:
        if item in self._set:
            return False

        if len(self._queue) >= self._max_size:
            removed = self._queue.popleft()
            self._set.remove(removed)

        self._queue.append(item)
        self._set.add(item)
        return True

    def contains(self, item: T) -> bool:
        return item in self._set

    @property
    def count(self) -> int:
        return len(self._set)

    def clear(self):
        self._queue.clear()
        self._set.clear()