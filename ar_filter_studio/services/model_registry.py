"""ModelRegistry — discovers and validates AI weights in models/weights/."""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass
from pathlib import Path

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class ModelEntry:
    name: str
    path: Path
    sha256: str
    backend: str


class ModelRegistry:
    def __init__(self, root: Path) -> None:
        self.root = root
        self._entries: dict[str, ModelEntry] = {}

    def scan(self) -> dict[str, ModelEntry]:
        manifest = self.root / "manifest.json"
        if not manifest.exists():
            log.warning("no model manifest at %s", manifest)
            return {}
        spec = json.loads(manifest.read_text(encoding="utf-8"))
        for name, meta in spec.get("models", {}).items():
            path = self.root / meta["file"]
            if not path.exists():
                log.warning("missing weight file for %s: %s", name, path)
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != meta["sha256"]:
                log.error("checksum mismatch for %s — refusing to load", name)
                continue
            self._entries[name] = ModelEntry(name, path, digest, meta.get("backend", "onnx"))
        return dict(self._entries)

    def get(self, name: str) -> ModelEntry | None:
        return self._entries.get(name)