"""Exporter — bundles a graph + weights into lens/WebAR/OBS targets."""

from __future__ import annotations

import json
import logging
import zipfile
from pathlib import Path

log = logging.getLogger(__name__)

_TARGETS = {"lens", "webar", "obs"}


class Exporter:
    def __init__(self, graph_path: Path, model_dir: Path) -> None:
        self.graph_path = graph_path
        self.model_dir = model_dir

    def export(self, target: str, out_dir: Path) -> Path:
        if target not in _TARGETS:
            raise ValueError(f"unsupported export target: {target!r}")
        out_dir.mkdir(parents=True, exist_ok=True)
        bundle = out_dir / f"ar-filter-{target}.zip"
        with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(self.graph_path, arcname="graph.json")
            zf.writestr("target.json", json.dumps({"target": target, "schema": 1}))
            for weight in self.model_dir.glob("*.onnx"):
                zf.write(weight, arcname=f"weights/{weight.name}")
        log.info("exported %s bundle -> %s", target, bundle)
        return bundle