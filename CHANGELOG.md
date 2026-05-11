# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] — 2026-05-11

### Added

- **`repo_visibility_flip` risky-op category** — the compliance classifier now matches `gh repo edit <repo> --visibility (public|internal)`. This kind of action is effectively irreversible due to search-index/Wayback caching, so it deserves the same HITL nudge as `force_push_main`. Default gate is `warn`.
- **Real `score_security` in the python drift preset** — `bandit` runs against `lib/` and `hooks/`. Medium severity costs 0.1, high costs 0.5. Previously a silent no-op stub (`auto=0.0, confidence=0.0`).
- **`.mek/drift-baseline.json` seeded for MEK itself** — checked in. Manual grades left null so users can hand-grade later; current auto-scores: tests=1.0, lint=1.0, coverage=0.76, security=1.0.

### Fixed

- `lib/source_app_detect.has_cosmictasha` now refuses non-http/https URLs (bandit B310). Previously `file://` and other schemes would have been accepted.
- `lib/drift_scoring/python_preset.py` now uses `sys.executable` instead of literal `"python"` when spawning subprocesses — fixes the case where `PATH` resolves `python` to a different interpreter than the one running MEK.

### Dependencies

- New dev dep: `bandit>=1.7`. CI install via `pip install -e ".[dev]"` already covers it.

## [0.1.1] — 2026-05-11

### Fixed

- `lib.decimal_math.to_decimal` now rejects `float` with `TypeError` (was silently routing through `str(value)`, contradicting the module's "no floats" contract).
- `lib.decimal_math.sum_money` now quantizes its result to `MONEY_PLACES` on exit — "money in, money out."
- `lib.decimal_math.rebalance` now:
  - raises `ValueError("weights must not be empty")` for empty input
  - raises `ValueError("weights must be non-negative")` for negative weights
  - quantizes the residual bucket (was carrying excess precision when `total` had > 4 places)

All four fixes surfaced from a dogfood pass: running the new `maxexpresskit:ledger` subagent on `lib/decimal_math.py` itself.

## [0.1.0] — 2026-05-10

### Added

- Three distilled guardrails: `compliance`, `drift`, `ledger`.
- Three named subagents matching each guardrail.
- `using-mek` entry skill.
- Slash commands: `/mek-init`, `/mek-status`, `/mek-drift`, `/mek-compliance-audit`.
- Layer 2 wrapper stubs: `/mek-books`, `/mek-soc2`.
- Hooks: `pre_risky_op.py` (warn-only default), `money_math_guard.py`, `post_task_drift.py`.
- `lib/decimal_math.py` ported from BookKeeper with new helpers (`sum_money`, `pct_of`, `rebalance`).
- `lib/drift_scoring/` (grades, baseline, python preset).
- `lib/source_app_detect.py` for CosmicTasha / ScoreRift / BookKeeper.
- `lib/config.py` for `mek.toml`.
- `scaffold/` payload for `/mek-init`.
- Docs: concepts + per-guardrail + source-app integration.
- CI: pytest + ruff on Ubuntu + Windows, Python 3.11 and 3.12.

### Stubbed

- `skills/ledger-companion/` — placeholder for the v0.2.0 mini-ledger.
- Full Layer 2 pass-through wrappers — v0.2.0.

### Known limitations

- Drift preset is Python-only.
- CosmicTasha integration is a localhost probe, not a full handshake.
- No telemetry. Noise suppression is config-driven (`mek.toml > [compliance.gates]`).
