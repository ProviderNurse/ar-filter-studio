"""Structured logging: console (rich) + rotating JSONL session log."""

from __future__ import annotations

import json
import logging
import logging.handlers
import time
from pathlib import Path

from rich.logging import RichHandler

_SESSION_DIR = Path("logs")


class JsonlFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": round(time.time(), 3),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(verbose: int = 0) -> None:
    level = logging.WARNING - min(verbose, 2) * 10
    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()

    console = RichHandler(rich_tracebacks=True, show_path=False)
    console.setLevel(level)
    root.addHandler(console)

    _SESSION_DIR.mkdir(exist_ok=True)
    session = _SESSION_DIR / f"session-{int(time.time())}.jsonl"
    fileh = logging.handlers.RotatingFileHandler(
        session, maxBytes=8 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    fileh.setFormatter(JsonlFormatter())
    fileh.setLevel(logging.DEBUG)
    root.addHandler(fileh)