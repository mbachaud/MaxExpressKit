---
name: drift
description: Use after PR-sized work completes (or on /mek-drift) to compare auto scores against .mek/drift-baseline.json and surface divergences > 0.15.
---

# drift — auto-vs-baseline divergence detection

## When to invoke

- Stop hook fires after a meaningful chunk of work (post_task_drift.py).
- User runs `/mek-drift`.

## What it does

1. Loads `.mek/drift-baseline.json` (created by `/mek-drift init`).
2. Runs the Python preset auto-scorers: test pass rate, lint, coverage. Security stays manual-only at v0.1.0.
3. Compares to manual baseline. Flags any dimension where:
   - `|auto - manual| > divergence_threshold` (default 0.15) AND `confidence >= min_confidence` (default 0.5), OR
   - `auto < floor` (ratchet violation).

## Resolution paths

- `/mek-drift accept` — agree with auto, update manual to match.
- `/mek-drift ack` — disagree with auto, dismiss this flag (record in baseline metadata).
- Re-audit manually and update the baseline.

## Config

`mek.toml > [drift]`:

```toml
[drift]
baseline_file = ".mek/drift-baseline.json"
preset = "python"
divergence_threshold = 0.15
min_confidence = 0.5
auto_run_on_stop = true
```
