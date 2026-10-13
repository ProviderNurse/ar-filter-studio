"""Command-line entry for ar-filter-studio.

Parses args, initializes logging, and hands control to the app runner.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from ar_filter_studio.bootstrap.logging_setup import configure_logging
from ar_filter_studio.config.loader import load_config
from ar_filter_studio.core.app import AppRunner

log = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ar-filter-studio",
        description="AI AR filter generator — live face/body tracking + effect graph.",
    )
    p.add_argument("--profile", default="default", help="config profile name")
    p.add_argument("--config", type=Path, default=None, help="explicit config path")
    p.add_argument("--graph", type=Path, default=None, help="effect graph JSON to load")
    p.add_argument("--headless", action="store_true", help="run without preview window")
    p.add_argument("--export", choices=["lens", "webar", "obs"], default=None)
    p.add_argument("--verbose", "-v", action="count", default=0)
    return p


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    configure_logging(verbose=args.verbose)

    try:
        config = load_config(profile=args.profile, explicit=args.config)
    except FileNotFoundError as exc:
        log.error("config not found: %s", exc)
        return 2

    runner = AppRunner(config=config, graph_path=args.graph, headless=args.headless)
    try:
        runner.run()
    except KeyboardInterrupt:
        log.info("interrupted by user — shutting down cleanly")
        return 130
    finally:
        runner.shutdown()

    if args.export:
        log.info("export requested: %s", args.export)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))