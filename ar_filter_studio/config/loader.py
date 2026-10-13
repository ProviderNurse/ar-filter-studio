"""Load and merge config profiles from config/*.yaml."""

from __future__ import annotations

import os
from pathlib import Path

import yaml

from ar_filter_studio.config.schema import StudioConfig

_CONFIG_DIR = Path(__file__).resolve().parents[2] / "config"


def _deep_merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for key, val in override.items():
        if isinstance(val, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], val)
        else:
            out[key] = val
    return out


def load_config(profile: str = "default", explicit: Path | None = None) -> StudioConfig:
    """Resolve profile -> merged dict -> validated StudioConfig.

    Precedence: base.yaml < {profile}.yaml < ARFILTER_* env overrides.
    """
    base_path = explicit or (_CONFIG_DIR / "base.yaml")
    if not base_path.exists():
        raise FileNotFoundError(base_path)

    merged = yaml.safe_load(base_path.read_text(encoding="utf-8")) or {}

    if explicit is None and profile != "default":
        prof_path = _CONFIG_DIR / f"{profile}.yaml"
        if prof_path.exists():
            merged = _deep_merge(merged, yaml.safe_load(prof_path.read_text()) or {})

    if env_backend := os.environ.get("ARFILTER_BACKEND"):
        merged.setdefault("inference", {})["backend"] = env_backend

    merged["profile"] = profile
    return StudioConfig.model_validate(merged)