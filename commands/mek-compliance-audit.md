---
description: Audit compliance artifacts for staleness and unsigned HITL approvals.
argument-hint: "[--write <path>] [--soft]"
---

# /mek-compliance-audit $ARGUMENTS

Walk `compliance/` and produce a markdown report.

For each file:

- Check `mtime`. Mark `stale` if older than `compliance.staleness_days` (default 90) AND no `last_reviewed:` frontmatter within the window.
- For HITL approval files: check for a `Signed off by:` line.

**Privacy check: tracked approvals.** HITL approval files frequently contain names, infrastructure details, and other sensitive data, so the default scaffold gitignores `compliance/approvals/`. Run `git ls-files compliance/approvals/` — if it returns any paths, surface them as a warning (`tracked HITL approvals detected: <paths>. Confirm these are intentionally version-controlled, or add to compliance/.gitignore.`). Treat this as advisory (does not by itself set exit 1) unless the user passes `--strict`, in which case tracked unredacted approvals fail the audit.

Output: a markdown table to stdout plus a separate "Tracked approvals" section when present. With `--write <path>`, also write the report to that file.

Exit code:

- `0` if everything is fresh and signed.
- `1` if any artifact is stale or unsigned, OR if `--strict` is passed and any tracked file lives under `compliance/approvals/`.
- `--soft` coerces exit to `0` (for CI advisory mode).
