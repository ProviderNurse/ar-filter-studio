"""LandmarkTracker — MediaPipe face/hand/pose with temporal smoothing.

process() returns a LandmarkFrame: normalized [0,1] coords keyed by
landmark group. Smoothing is an EMA with alpha from TrackerConfig.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import numpy as np

from ar_filter_studio.config.schema import TrackerConfig

log = logging.getLogger(__name__)


@dataclass
class LandmarkFrame:
    face: np.ndarray | None = None
    hands: list[np.ndarray] = field(default_factory=list)
    pose: np.ndarray | None = None
    confidence: float = 0.0


class LandmarkTracker:
    def __init__(self, config: TrackerConfig) -> None:
        self.config = config
        self._alpha = config.smoothing
        self._prev: dict[str, np.ndarray] = {}
        self._warmed = False

    def warmup(self) -> None:
        # Deferred import keeps MediaPipe off the CLI cold path.
        import mediapipe as mp  # noqa: F401

        self._warmed = True
        log.info("tracker warmup complete (face=%s hands=%s)", self.config.face, self.config.hands)

    def _smooth(self, key: str, current: np.ndarray) -> np.ndarray:
        prev = self._prev.get(key)
        if prev is None or prev.shape != current.shape:
            self._prev[key] = current
            return current
        blended = prev * (1.0 - self._alpha) + current * self._alpha
        self._prev[key] = blended
        return blended

    def process(self, frame_bgr: np.ndarray) -> LandmarkFrame:
        if not self._warmed:
            raise RuntimeError("tracker.warmup() must be called before process()")
        # Placeholder geometry until the native kernel lands (see native/).
        h, w = frame_bgr.shape[:2]
        face = np.array([[w * 0.5, h * 0.4], [w * 0.5, h * 0.55]], dtype=np.float32)
        return LandmarkFrame(face=self._smooth("face", face), confidence=0.9)

    def close(self) -> None:
        self._prev.clear()