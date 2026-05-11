# Source-app integration (Layer 2)

MEK's three guardrails distill the agent surface of three larger apps:

| Guardrail | Source app | What integration enables |
|---|---|---|
| `compliance` | [CosmicTasha](https://github.com/mbachaud/CosmicTasha) (SOC2 doc generator) | Send compliance artifacts through CT's HITL flow. |
| `drift` | [ScoreRift](https://github.com/mbachaud/two-brain-audit) (two-brain auditor) | Defer scoring to ScoreRift's richer preset library + persistent history. |
| `ledger` | [BookKeeper](https://github.com/mbachaud/BookKeeper) (double-entry accounting) | Full ledger operations, tax exports, multi-tenant SaaS mode. |

## v0.1.0

Stub-only. `/mek-books` and `/mek-soc2` detect the source app via `lib.source_app_detect` and print where they'd dispatch when full pass-through ships.

## v0.2.0 (planned)

Full pass-through: when the source app is detected, the wrapper command shells out to it and returns the result. When absent, MEK falls back to the distilled Layer 1.

## Detection

| App | Detection method |
|---|---|
| ScoreRift | `shutil.which("scorerift")` |
| BookKeeper | `shutil.which("bookkeeper")` |
| CosmicTasha | HTTP probe `http://localhost:3000/api/health` (2s timeout). |

Override the defaults in `mek.toml > [source_apps]`.
