# HITL Approval Template

Use this when an operation requires Human-In-The-Loop approval.

| Field | Value |
| --- | --- |
| Date (UTC) | YYYY-MM-DDTHH:MMZ |
| Operator | <name / agent ID> |
| Approver | <human name + role> |
| Operation | <category — `rm_rf`, `deploy`, `schema_migration`, `money_write`, `force_push_main`, `repo_visibility_flip`> |
| Target | <file / db / cluster / branch> |
| Rationale | <one paragraph: what, why, blast radius> |
| Rollback plan | `how to undo if it goes wrong` |
| Signed off by | <name + timestamp> |

## How to use

1. Fill in this template (copy as a new dated file in `compliance/approvals/`, or inline in `DECISION_LOG.md`).
2. Have the named approver respond in writing (PR comment, Slack thread, signed commit).
3. Reference the approval in your commit message or PR description.
