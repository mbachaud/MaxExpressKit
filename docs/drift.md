# drift

Compare deterministic auto-scores (tests, lint, coverage) against manual scores in `.mek/drift-baseline.json`.

Divergence rule (ScoreRift-compatible): flag when

- `|auto - manual_as_float| > divergence_threshold` (default 0.15), AND
- `confidence ≥ min_confidence` (default 0.5).

Also flag any dimension where `auto < floor` (ratchet — regardless of confidence).

## Workflow

1. `/mek-drift init` — seed the baseline.
2. Open the baseline; fill in `manual` (letter grade) for the dimensions you care about.
3. Work normally. Stop hook checks for divergences after PR-sized changes.
4. `/mek-drift status` — on-demand check.
5. `/mek-drift accept` or `/mek-drift ack` — resolve a flagged dimension.

## v0.1.0 preset

Only `python` is shipped. Other presets (JS, Go, Rust) are v0.2.0.
