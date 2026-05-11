# Concepts

MEK is a Claude Code plugin that ships three **guardrails** — ambient agent helpers that nudge, warn, or block to keep the agent honest in three failure modes.

## The three guardrails

| Guardrail | Failure it prevents |
|---|---|
| `compliance` | Agent runs irreversible ops without recording HITL approval. |
| `drift` | Code rots away from a baseline without anyone noticing. |
| `ledger` | Money math gets corrupted by Python `float` rounding. |

## The three layers

1. **Distilled core** — works on any project; no source-app dependency.
2. **Wrappers** — light up when CosmicTasha / ScoreRift / BookKeeper are installed and defer to them.
3. **Scaffold** — `/mek-init` drops `mek.toml` + `compliance/` templates into your project.

## Quiet by default

Skills nudge; hooks WARN. To escalate to hard blocks, set `mek.toml > [compliance.gates] > <op> = "block"`.

## Config schema

See `scaffold/mek.toml` for the canonical example with every section documented.
