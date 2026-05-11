# compliance

Ambient HITL/audit nudge. Triggers on six risky-op categories:

- `rm_rf`, `deploy`, `schema_migration`, `money_write`, `force_push_main`, `repo_visibility_flip`.

For each, the `pre_risky_op.py` hook checks `mek.toml > [compliance.gates] > <op>`:

- `off` — silent.
- `warn` — print a reminder; the agent continues.
- `block` — exit non-zero; Claude is told the action was denied.

To record a decision, copy `compliance/HITL_TEMPLATE.md` and append the row to `compliance/DECISION_LOG.md`.

Run `/mek-compliance-audit` to find stale artifacts and unsigned approvals.

## HITL approvals and privacy

`compliance/approvals/` is the conventional landing zone for signed HITL records — one file per approval. These files frequently contain names, infrastructure details, and rationale you probably don't want in public git history.

MEK's scaffold (`/mek-init`) drops a `compliance/.gitignore` that ignores `approvals/` by default. To track a specific approval (e.g., after redacting it), add an explicit negation:

```gitignore
approvals/
!approvals/2026-05-11-redacted-public.md
```

`/mek-compliance-audit` includes an advisory check that surfaces any files currently tracked under `compliance/approvals/` so you can confirm the exposure is intentional. Pass `--strict` to fail the audit on any tracked approval.

## Hardening: block visibility flips when approvals exist

By default `repo_visibility_flip` is gated as `warn` — the operator is reminded but can proceed. Two ways to tighten this if your project keeps HITL approvals on disk:

**Static block (simplest, works today.)** In `mek.toml`:

```toml
[compliance.gates]
repo_visibility_flip = "block"
```

Every `gh repo edit … --visibility public|internal` is denied until you flip the gate back to `warn` for the specific run. The decision then lives in `DECISION_LOG.md` as proof that someone consciously unlocked it.

**Conditional block (state-aware, ~15-line hook).** If you only want the hard block when `compliance/approvals/` has content on disk, wrap `pre_risky_op.py` with a project-local hook that escalates dynamically. Sketch:

```python
# .claude/hooks/visibility_guard.py
import json, subprocess, sys
from pathlib import Path

payload = json.load(sys.stdin)
cmd = payload.get("tool_input", {}).get("command", "")
if "gh repo edit" not in cmd or "--visibility" not in cmd:
    sys.exit(0)
approvals = Path("compliance/approvals")
if approvals.exists() and any(approvals.iterdir()):
    print("[guard] approvals/ has content; refusing visibility flip.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
```

Register it as a `PreToolUse` hook with matcher `Bash`. This is opt-in territory — MEK ships the static gate; the conditional version is a project's choice.
