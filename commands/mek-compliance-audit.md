---
description: Audit compliance artifacts for staleness and unsigned HITL approvals.
argument-hint: "[--write <path>] [--soft]"
---

# /mek-compliance-audit $ARGUMENTS

Walk `compliance/` and produce a markdown report.

For each file:

- Check `mtime`. Mark `stale` if older than `compliance.staleness_days` (default 90) AND no `last_reviewed:` frontmatter within the window.
- For HITL approval files: check for a `Signed off by:` line.

Output: a markdown table to stdout. With `--write <path>`, also write the report to that file.

Exit code:

- `0` if everything is fresh and signed.
- `1` if any artifact is stale or unsigned.
- `--soft` coerces exit to `0` (for CI advisory mode).
