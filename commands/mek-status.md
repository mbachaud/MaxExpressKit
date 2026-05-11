---
description: Show active MEK guardrails and source-app detection.
---

# /mek-status

Print to stdout (always exit 0):

1. Active guardrails (read from `mek.toml > [compliance.gates]` and `[mek] strictness`).
2. Source-app detection via `lib.source_app_detect`.
3. Presence of `mek.toml` and `.mek/drift-baseline.json`.

Example output:

```
MaxExpressKit — status

Guardrails
  compliance        strictness=warn       gates: rm_rf=warn deploy=warn money_write=block
  drift             auto_run_on_stop=true  baseline: present (4 dims)
  ledger            warn_on_float=true

Source apps (Layer 2)
  scorerift         not detected
  bookkeeper        detected at /usr/local/bin/bookkeeper (v0.3.0)
  cosmictasha       not detected

Project files
  mek.toml          present
  .mek/             present (1 file)
```
