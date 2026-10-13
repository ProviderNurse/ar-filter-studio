"""Geometry helpers for landmark math."""

from __future__ import annotations

import numpy as np


def centroid(points: np.ndarray) -> np.ndarray:
    if points.size == 0:
        raise ValueError("centroid of empty point set")
    return points.mean(axis=0)


def bbox(points: np.ndarray) -> tuple[int, int, int, int]:
    xs, ys = points[:, 0], points[:, 1]
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def scale_to_frame(points: np.ndarray, width: int, height: int) -> np.ndarray:
    scaled = points.copy()
    scaled[:, 0] *= width
    scaled[:, 1] *= height
    return scaled