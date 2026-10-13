"""Typed config schema for ar-filter-studio (pydantic v2)."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

BackendKind = Literal["cpu", "onnx-cuda", "onnx-directml", "torch"]


class CaptureConfig(BaseModel):
    device_index: int = 0
    width: int = 1280
    height: int = 720
    fps: int = 30
    mirror: bool = True


class TrackerConfig(BaseModel):
    face: bool = True
    hands: bool = True
    pose: bool = False
    smoothing: float = Field(0.35, ge=0.0, le=1.0)
    max_faces: int = Field(2, ge=1, le=8)


class InferenceConfig(BaseModel):
    backend: BackendKind = "onnx-cuda"
    model_dir: Path = Path("models/weights")
    allow_cloud: bool = False
    cloud_endpoint: str | None = None


class RenderConfig(BaseModel):
    preview: bool = True
    virtual_camera: bool = False
    target_fps: int = 60
    resolution_scale: float = Field(1.0, ge=0.25, le=2.0)


class StudioConfig(BaseModel):
    profile: str = "default"
    capture: CaptureConfig = CaptureConfig()
    tracker: TrackerConfig = TrackerConfig()
    inference: InferenceConfig = InferenceConfig()
    render: RenderConfig = RenderConfig()
    graph_path: Path | None = None