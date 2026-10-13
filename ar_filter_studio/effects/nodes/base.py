"""EffectNode ABC — the contract every filter node implements.

prepare() runs once at compile; render() runs per frame and must be
pure with respect to the input frame (return a new array or mutate a
copy). release() frees GPU/native resources.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from ar_filter_studio.tracking.tracker import LandmarkFrame


class EffectNode(ABC):
    name: str = "effect"

    def prepare(self) -> None:  # noqa: B027 - optional hook
        return None

    @abstractmethod
    def render(self, frame_bgr: np.ndarray, landmarks: LandmarkFrame) -> np.ndarray:
        raise NotImplementedError

    def release(self) -> None:  # noqa: B027 - optional hook
        return None