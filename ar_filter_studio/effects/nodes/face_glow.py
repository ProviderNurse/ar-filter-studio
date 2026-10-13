"""FaceGlowNode — soft additive glow masked to tracked face landmarks."""

from __future__ import annotations

import cv2
import numpy as np

from ar_filter_studio.effects.nodes.base import EffectNode
from ar_filter_studio.tracking.tracker import LandmarkFrame


class FaceGlowNode(EffectNode):
    name = "face_glow"

    def __init__(self, radius: int = 48, intensity: float = 0.6, tint: tuple[int, int, int] = (255, 200, 120)) -> None:
        self.radius = radius
        self.intensity = float(np.clip(intensity, 0.0, 1.0))
        self.tint = tint
        self._kernel: np.ndarray | None = None

    def prepare(self) -> None:
        k = self.radius * 2 + 1
        self._kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))

    def render(self, frame_bgr: np.ndarray, landmarks: LandmarkFrame) -> np.ndarray:
        if landmarks.face is None or self._kernel is None:
            return frame_bgr
        mask = np.zeros(frame_bgr.shape[:2], dtype=np.uint8)
        for x, y in landmarks.face.astype(int):
            cv2.circle(mask, (int(x), int(y)), self.radius, 255, -1)
        mask = cv2.GaussianBlur(mask, (0, 0), self.radius / 3)
        tint_layer = np.full_like(frame_bgr, self.tint)
        return cv2.addWeighted(frame_bgr, 1.0, cv2.bitwise_and(tint_layer, tint_layer, mask=mask), self.intensity, 0)