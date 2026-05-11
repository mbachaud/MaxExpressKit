---
name: compliance
description: Use when the agent is about to perform a risky operation (destructive shell, deploy, schema migration, money write, force-push). Reminds to record HITL approval and points at compliance/ templates.
---

# compliance — HITL & audit nudge

## When to invoke

Auto-activates when the agent is about to run a classified risky op:

- `rm_rf` — destructive shell deletion
- `deploy` — `kubectl apply`, `docker compose up`, `terraform apply`, etc.
- `schema_migration` — file in `migrations/`
- `money_write` — `INSERT/UPDATE/DELETE` against money tables
- `force_push_main` — `git push --force` to `main` / `master`

## What to do

1. Check whether the project has `compliance/HITL_TEMPLATE.md`. If not, prompt the user to run `/mek-init`.
2. Ask the user: "Has HITL approval been recorded for this operation? (Y/n)"
3. If yes, append a row to `compliance/DECISION_LOG.md` with date, operator, op category, and short rationale.
4. Proceed.

## Strictness

Quiet-by-default. The hook will WARN. To escalate to a hard block, set `mek.toml > [compliance.gates] > <op> = "block"`.
