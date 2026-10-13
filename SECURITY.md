# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | ✅ |
| 0.5.x   | ✅ |
| < 0.5   | ❌ |

## Reporting a vulnerability

Email `security@ar-filter-studio.dev` with a description, repro steps, and
the affected component (`tracker`, `effects`, `export`, `native_bridge`,
`capture`, or `remote`). We aim to acknowledge within 72 hours.

Please do **not** open public issues for memory-safety bugs in `native/`
or for anything in `remote/` that could allow arbitrary code execution
via a crafted lens bundle.

## Threat model

`ar-filter-studio` loads third-party effect bundles and AI model weights.
Treat all bundle contents as untrusted:

- Lens bundles are sandboxed; scripted nodes run in a restricted
  subinterpreter with no filesystem or network access.
- ONNX/TFLite weights are validated against a manifest before load.
- The `remote/` lens-market client verifies signatures before install.
- Webcam and screen-capture frames never leave the machine unless the user
  explicitly enables cloud inference in `config/local.yaml`.

## Out of scope

- Physical camera tampering.
- GPU driver vulnerabilities.
- Effects that are simply ugly.