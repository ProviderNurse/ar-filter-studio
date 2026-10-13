"""Entry point: `python -m ar_filter_studio`."""

from __future__ import annotations

import sys

from ar_filter_studio.bootstrap.cli import main


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))