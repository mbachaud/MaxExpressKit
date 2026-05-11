# compliance

Ambient HITL/audit nudge. Triggers on five risky-op categories:

- `rm_rf`, `deploy`, `schema_migration`, `money_write`, `force_push_main`.

For each, the `pre_risky_op.py` hook checks `mek.toml > [compliance.gates] > <op>`:

- `off` — silent.
- `warn` — print a reminder; the agent continues.
- `block` — exit non-zero; Claude is told the action was denied.

To record a decision, copy `compliance/HITL_TEMPLATE.md` and append the row to `compliance/DECISION_LOG.md`.

Run `/mek-compliance-audit` to find stale artifacts and unsigned approvals.
