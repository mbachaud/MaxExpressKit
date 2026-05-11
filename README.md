# MaxExpressKit (MEK)

> Three guardrails for Claude Code: **compliance**, **drift**, **ledger**.

MEK is a Claude Code plugin that ships ambient guardrails for agent work — distilled from three full apps (CosmicTasha, ScoreRift, BookKeeper).

## Why

Agents fail in patterns:

- They run irreversible ops without recording HITL approval.
- They drift away from a code-quality baseline without anyone noticing.
- They use Python `float` for money and silently round.

MEK ships one ambient skill per failure mode, plus matching subagents you can delegate to via `Task`, plus opt-in hard-gate hooks.

## Install

```bash
/plugin install mbachaud/MaxExpressKit
```

## Scaffold a project

```bash
/mek-init
```

Drops `mek.toml` + `compliance/` templates into the current directory. Then:

```bash
/mek-drift init        # seed the drift baseline
/mek-status            # see what's active
```

## The three guardrails

| Guardrail | When it fires | What it does |
|---|---|---|
| **compliance** | Before `rm -rf`, deploy, schema migration, money write, force-push | Nudges to record HITL approval; can hard-block via config. |
| **drift** | After PR-sized work (Stop hook) or `/mek-drift` | Compares auto scores (tests, lint, coverage) against your manual baseline. |
| **ledger** | When the agent touches `amount_*`, `price_*`, `balance_*` identifiers | Enforces `Decimal`-only math; warns on float-money assignments. |

## Quiet by default

Skills nudge; hooks WARN. To escalate to hard blocks on specific ops, edit `mek.toml`:

```toml
[compliance.gates]
rm_rf = "block"          # require HITL before any rm -rf
force_push_main = "block"
```

## Layered architecture

1. **Distilled core** — works anywhere; no source-app dependency.
2. **Wrappers** — `/mek-books`, `/mek-soc2` light up when CosmicTasha / ScoreRift / BookKeeper are installed. v0.1.0 ships stubs; v0.2.0 ships full pass-through.
3. **Scaffold** — `/mek-init` lays down your project-level config.

## Docs

- [Concepts](docs/concepts.md)
- [Compliance guardrail](docs/compliance.md)
- [Drift guardrail](docs/drift.md)
- [Ledger guardrail](docs/ledger.md)
- [Source-app integration](docs/source-app-integration.md)

## License

Apache 2.0 — see [LICENSE](LICENSE).
