---
name: using-mek
description: Use when starting any conversation in a project where MEK is installed - announces the three guardrails (compliance, drift, ledger) and how to invoke them.
---

# Using MaxExpressKit

MEK ships three guardrails that activate automatically in projects where it's installed:

| Guardrail | When it fires | What it does |
|---|---|---|
| `compliance` | Before risky ops (`rm -rf`, deploy, money writes, force-push) | Injects an HITL reminder and points at applicable compliance docs. |
| `drift` | After PR-sized work (Stop hook) or `/mek-drift` | Compares auto scores (tests/lint/coverage/security) against `.mek/drift-baseline.json`. |
| `ledger` | When the agent touches money-shaped identifiers (`amount_*`, `price_*`, `balance_*`) | Enforces `Decimal`-only math; warns on float arithmetic. |

## Slash commands

- `/mek-init` — drop `mek.toml` + `compliance/` templates into the current project.
- `/mek-status` — show active guardrails and source-app detection.
- `/mek-drift` — run a drift check on demand.
- `/mek-compliance-audit` — audit compliance artifacts for staleness.
- `/mek-books`, `/mek-soc2` — Layer 2 stubs; light up when BookKeeper / CosmicTasha are installed.

## Config

Project-level config lives in `mek.toml`. See [`docs/concepts.md`](../../docs/concepts.md) for the schema.

## Default behavior

Quiet. Skills nudge; hooks WARN, never block. Escalate per-op to `block` via `mek.toml > [compliance.gates]`.
