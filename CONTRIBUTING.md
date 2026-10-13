# Contributing to ar-filter-studio

Thanks for wanting to build with us. `ar-filter-studio` is a Windows desktop
tool that turns a webcam feed into a live AI augmented-reality filter rig:
face/body tracking, generative effect graphs, and one-click export to
Snapchat-style lens bundles, WebAR, and OBS virtual camera.

## Ground rules

- Python 3.11+ for the desktop app. Native tracking kernels live in
  `native/` (C++/C#/Java bindings are welcome — see `bindings/`).
- Every PR must run `pytest -q` and `ruff check .` clean before review.
- Keep the effect graph declarative. If you're hardcoding a filter in the
  render loop, you're doing it wrong — add a node to `effects/nodes/`.
- One feature per PR. Small diffs land fast.

## Dev environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
python -m ar_filter_studio --profile dev
```

## Adding an effect node

1. Subclass `effects.nodes.base.EffectNode`.
2. Declare `inputs` / `outputs` as typed `FrameSpec` ports.
3. Register it in `effects/registry.py`.
4. Add a smoke test under `tests/`.

## Code style

- Type hints everywhere. `mypy --strict` on `ar_filter_studio/`.
- No bare `except`. Log and re-raise or handle explicitly.
- Naming: intention-revealing. `landmark_buffer`, not `data`.
- Native interop goes through `native_bridge/`, never called inline.

## Commit messages

`area: short imperative summary` — e.g. `tracker: add iris landmark smoothing`.

## Reporting bugs

Open an issue with: OS build, GPU + driver, capture device, the effect
graph JSON, and the `logs/session-*.jsonl` tail.