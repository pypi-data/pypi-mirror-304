import time
from typing import Dict


class StopWatch:
    def __init__(self):
        self.reset()

    def reset(self):
        self.start_time = time.time()

    @property
    def elapsed_milliseconds(self) -> int:
        return int((time.time() - self.start_time) * 1000)


class StopWatchContainer:
    def __init__(self):
        self._stop_watch_map: Dict[str, StopWatch] = {}

    def hit_timer(self, key: str, time_ms: int) -> bool:
        if key not in self._stop_watch_map:
            stopwatch = StopWatch()
            self._stop_watch_map[key] = stopwatch
            return True

        return self._stop_watch_map[key].elapsed_milliseconds >= time_ms

    def reset(self, key: str):
        if key not in self._stop_watch_map:
            stopwatch = StopWatch()
            self._stop_watch_map[key] = stopwatch
        else:
            self._stop_watch_map[key].reset()