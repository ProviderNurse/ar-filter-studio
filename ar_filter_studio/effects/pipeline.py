"""EffectPipeline — topological execution of a node graph per frame."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import numpy as np

from ar_filter_studio.config.schema import StudioConfig
from ar_filter_studio.effects.registry import get_node
from ar_filter_studio.effects.nodes.base import EffectNode
from ar_filter_studio.tracking.tracker import LandmarkFrame

log = logging.getLogger(__name__)


class EffectPipeline:
    def __init__(self, nodes: list[EffectNode] | None = None) -> None:
        self.nodes: list[EffectNode] = nodes or []

    @classmethod
    def from_config(cls, config: StudioConfig) -> "EffectPipeline":
        if config.graph_path and config.graph_path.exists():
            return cls._from_graph_file(config.graph_path)
        return cls()

    @classmethod
    def _from_graph_file(cls, path: Path) -> "EffectPipeline":
        spec = json.loads(path.read_text(encoding="utf-8"))
        nodes = [get_node(n["type"])(**n.get("params", {})) for n in spec["nodes"]]
        return cls(nodes)

    def load_graph(self, path: Path) -> None:
        self.nodes = self._from_graph_file(path).nodes
        log.info("loaded effect graph: %s (%d nodes)", path.name, len(self.nodes))

    def compile(self) -> None:
        for node in self.nodes:
            node.prepare()

    def apply(self, frame_bgr: np.ndarray, landmarks: LandmarkFrame) -> np.ndarray:
        out = frame_bgr
        for node in self.nodes:
            out = node.render(out, landmarks)
        return out

    def release(self) -> None:
        for node in self.nodes:
            node.release()
        self.nodes.clear()