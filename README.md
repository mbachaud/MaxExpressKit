# MaxExpressKit (MEK)

> Three guardrails for Claude Code: **compliance**, **drift**, **ledger**.

MEK is a Claude Code plugin that ships ambient guardrails for agent work:

- `compliance` — nudges before risky ops and reminds HITL approval is needed.
- `drift` — runs after PR-sized work, compares auto scores vs your baseline.
- `ledger` — enforces `Decimal`-only math so floats can't silently corrupt money.

## Install

```bash
/plugin install mbachaud/MaxExpressKit
```

## Scaffold a project

```bash
/mek-init
```

Drops `mek.toml` + `compliance/` templates into the current directory.

## Status

Pre-v0.1.0. Documentation, screenshots, and demo GIF land before tag.
