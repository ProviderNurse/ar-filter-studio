"""AppRunner — wires capture -> session -> preview/virtual-camera."""

from __future__ import annotations

import logging
from pathlib import Path

from ar_filter_studio.capture.webcam import WebcamSource
from ar_filter_studio.config.schema import StudioConfig
from ar_filter_studio.core.session import FilterSession
from ar_filter_studio.render.preview import PreviewWindow

log = logging.getLogger(__name__)


class AppRunner:
    def __init__(self, config: StudioConfig, graph_path: Path | None = None, headless: bool = False) -> None:
        self.config = config
        self.graph_path = graph_path or config.graph_path
        self.headless = headless
        self._session: FilterSession | None = None
        self._capture: WebcamSource | None = None
        self._preview: PreviewWindow | None = None

    def run(self) -> None:
        self._capture = WebcamSource(self.config.capture)
        self._session = FilterSession(self.config)
        if self.graph_path:
            self._session.pipeline.load_graph(self.graph_path)
        self._session.open()

        if not self.headless:
            self._preview = PreviewWindow(self.config.render)

        log.info("entering render loop (headless=%s)", self.headless)
        while self._capture.is_open:
            frame = self._capture.read()
            if frame is None:
                continue
            composited = self._session.step(frame)
            if self._preview:
                if not self._preview.show(composited):
                    break

    def shutdown(self) -> None:
        if self._preview:
            self._preview.close()
        if self._session:
            self._session.close()
        if self._capture:
            self._capture.close()