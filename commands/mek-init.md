---
description: Scaffold MEK into the current project — drops mek.toml + compliance/ templates.
argument-hint: "[--force]"
---

# /mek-init $ARGUMENTS

Copies `${CLAUDE_PLUGIN_ROOT}/scaffold/` into the current working directory.

Behavior:

1. If `mek.toml` already exists and `--force` is not passed, abort with a message and exit.
2. Otherwise, copy:
   - `scaffold/mek.toml` → `./mek.toml`
   - `scaffold/compliance/HITL_TEMPLATE.md` → `./compliance/HITL_TEMPLATE.md`
   - `scaffold/compliance/DECISION_LOG.md` → `./compliance/DECISION_LOG.md`
   - `scaffold/compliance/RISKY_OPS.yaml` → `./compliance/RISKY_OPS.yaml`
   - `scaffold/compliance/.gitignore` → `./compliance/.gitignore` (ignores `approvals/` by default — see [docs/compliance.md](../docs/compliance.md) for the rationale)
3. Print a summary of what was created and the next steps:
   - Run `/mek-drift init` to seed the drift baseline.
   - Open `compliance/RISKY_OPS.yaml` and add project-specific patterns.
   - HITL approvals belong under `compliance/approvals/`. That path is gitignored by default; add explicit `!approvals/<file>` negations to track redacted approvals.

This is a tool-using flow (Read, Write the files). Don't run shell `cp`.
