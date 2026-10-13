"""WebcamSource — OpenCV-backed capture with a bounded frame buffer.

Reads on the calling thread. `read()` returns the most recent frame or
None if the device dropped it. Frames are BGR uint8, shape (H, W, 3).
"""

from __future__ import annotations

import logging

import cv2
import numpy as np

from ar_filter_studio.config.schema import CaptureConfig

log = logging.getLogger(__name__)


class WebcamSource:
    def __init__(self, config: CaptureConfig) -> None:
        self.config = config
        self._cap = cv2.VideoCapture(config.device_index, cv2.CAP_DSHOW)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.height)
        self._cap.set(cv2.CAP_PROP_FPS, config.fps)
        if not self._cap.isOpened():
            raise RuntimeError(f"cannot open capture device {config.device_index}")

    @property
    def is_open(self) -> bool:
        return self._cap.isOpened()

    def read(self) -> np.ndarray | None:
        ok, frame = self._cap.read()
        if not ok or frame is None:
            log.debug("dropped frame from device %d", self.config.device_index)
            return None
        if self.config.mirror:
            frame = cv2.flip(frame, 1)
        return frame

    def close(self) -> None:
        if self._cap.isOpened():
            self._cap.release()