"""Timing helpers: rolling FPS meter and frame budget checks."""

from __future__ import annotations

import time
from collections import deque


class FpsMeter:
    def __init__(self, window: int = 60) -> None:
        self._stamps: deque[float] = deque(maxlen=window)

    def tick(self) -> None:
        self._stamps.append(time.perf_counter())

    @property
    def fps(self) -> float:
        if len(self._stamps) < 2:
            return 0.0
        span = self._stamps[-1] - self._stamps[0]
        return (len(self._stamps) - 1) / span if span > 0 else 0.0

    def over_budget(self, target_fps: int) -> bool:
        return self.fps > 0 and self.fps < target_fps * 0.9