"""Effect node registry — maps type names in graph JSON to classes."""

from __future__ import annotations

from ar_filter_studio.effects.nodes.base import EffectNode
from ar_filter_studio.effects.nodes.blur import BlurNode
from ar_filter_studio.effects.nodes.face_glow import FaceGlowNode
from ar_filter_studio.effects.nodes.particle import ParticleNode

_REGISTRY: dict[str, type[EffectNode]] = {
    "blur": BlurNode,
    "face_glow": FaceGlowNode,
    "particle": ParticleNode,
}


def get_node(node_type: str) -> type[EffectNode]:
    try:
        return _REGISTRY[node_type]
    except KeyError as exc:
        raise KeyError(f"unknown effect node type: {node_type!r}") from exc


def available() -> list[str]:
    return sorted(_REGISTRY)