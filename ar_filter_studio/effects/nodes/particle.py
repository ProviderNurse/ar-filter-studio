"""ParticleNode — spawns and integrates soft particles anchored to landmarks."""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

from ar_filter_studio.effects.nodes.base import EffectNode
from ar_filter_studio.tracking.tracker import LandmarkFrame


@dataclass
class _Particle:
    pos: np.ndarray
    vel: np.ndarray
    life: float
    hue: tuple[int, int, int]


class ParticleNode(EffectNode):
    name = "particle"

    def __init__(self, count: int = 64, spawn_rate: int = 4, color: tuple[int, int, int] = (120, 220, 255)) -> None:
        self.count = count
        self.spawn_rate = spawn_rate
        self.color = color
        self._particles: list[_Particle] = []

    def _spawn(self, origin: np.ndarray) -> None:
        if len(self._particles) >= self.count:
            self._particles.pop(0)
        vel = np.random.uniform(-1.5, 1.5, size=2)
        self._particles.append(_Particle(pos=origin.copy(), vel=vel, life=1.0, hue=self.color))

    def render(self, frame_bgr: np.ndarray, landmarks: LandmarkFrame) -> np.ndarray:
        if landmarks.face is not None and len(landmarks.face):
            for _ in range(self.spawn_rate):
                self._spawn(landmarks.face[0])
        out = frame_bgr.copy()
        for p in self._particles:
            p.pos += p.vel
            p.life -= 0.02
            if p.life > 0:
                radius = max(1, int(4 * p.life))
                cv2.circle(out, tuple(p.pos.astype(int)), radius, p.hue, -1)
        self._particles = [p for p in self._particles if p.life > 0]
        return out

    def release(self) -> None:
        self._particles.clear()