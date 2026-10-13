"""BlurNode — separable Gaussian blur, optional background-only mode."""

from __future__ import annotations

import cv2
import numpy as np

from ar_filter_studio.effects.nodes.base import EffectNode
from ar_filter_studio.tracking.tracker import LandmarkFrame


class BlurNode(EffectNode):
    name = "blur"

    def __init__(self, sigma: float = 8.0, background_only: bool = False) -> None:
        self.sigma = sigma
        self.background_only = background_only

    def render(self, frame_bgr: np.ndarray, landmarks: LandmarkFrame) -> np.ndarray:
        blurred = cv2.GaussianBlur(frame_bgr, (0, 0), self.sigma)
        if not self.background_only or landmarks.face is None:
            return blurred
        mask = np.zeros(frame_bgr.shape[:2], dtype=np.uint8)
        hull = cv2.convexHull(landmarks.face.astype(np.int32))
        cv2.fillConvexPoly(mask, hull, 255)
        return np.where(mask[..., None] > 0, frame_bgr, blurred)