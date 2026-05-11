# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
