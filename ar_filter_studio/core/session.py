"""FilterSession — owns capture, tracker, pipeline, and render loop state.

Lifecycle: open() -> step()* -> close(). Not thread-safe; the render loop
owns the session. Tracker inference may run on a worker via `submit()`.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

import numpy as np

from ar_filter_studio.config.schema import StudioConfig
from ar_filter_studio.effects.pipeline import EffectPipeline
from ar_filter_studio.tracking.tracker import LandmarkTracker

log = logging.getLogger(__name__)


@dataclass
class FrameStats:
    frame_index: int = 0
    capture_ms: float = 0.0
    track_ms: float = 0.0
    effect_ms: float = 0.0
    dropped: int = 0
    history: list[float] = field(default_factory=list)


class FilterSession:
    def __init__(self, config: StudioConfig) -> None:
        self.config = config
        self.tracker = LandmarkTracker(config.tracker)
        self.pipeline = EffectPipeline.from_config(config)
        self.stats = FrameStats()
        self._opened = False

    def open(self) -> None:
        self.tracker.warmup()
        self.pipeline.compile()
        self._opened = True
        log.info("session open: backend=%s fps=%d", self.config.inference.backend, self.config.render.target_fps)

    def step(self, frame_bgr: np.ndarray) -> np.ndarray:
        if not self._opened:
            raise RuntimeError("session not open; call open() first")
        t0 = time.perf_counter()
        landmarks = self.tracker.process(frame_bgr)
        t1 = time.perf_counter()
        out = self.pipeline.apply(frame_bgr, landmarks)
        t2 = time.perf_counter()

        self.stats.frame_index += 1
        self.stats.track_ms = (t1 - t0) * 1000
        self.stats.effect_ms = (t2 - t1) * 1000
        self.stats.history.append(self.stats.track_ms + self.stats.effect_ms)
        if len(self.stats.history) > 240:
            self.stats.history.pop(0)
        return out

    def close(self) -> None:
        self.pipeline.release()
        self.tracker.close()
        self._opened = False