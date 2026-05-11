"""PreToolUse hook: classify risky ops and apply mek.toml gate.

Exit codes follow Claude Code convention:
- 0: allow / warn (Claude continues)
- 2: block (Claude is told the action was denied)
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Make the plugin root importable so lib/* resolves regardless of cwd.
PLUGIN_ROOT = Path(os.environ.get("CLAUDE_PLUGIN_ROOT", Path(__file__).resolve().parents[2]))
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from lib.compliance_templates.risky_op_patterns import classify_risky_op
from lib.config import load_mek_toml


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return 0

    op = classify_risky_op(payload.get("tool_name", ""), payload.get("tool_input") or {})
    if op is None:
        return 0

    cfg = load_mek_toml(Path.cwd())
    gates = cfg.get("compliance", {}).get("gates", {})
    level = gates.get(op, "warn")

    if level == "off":
        return 0

    if level == "block":
        print(
            f"[compliance] blocked: {op} requires HITL approval. "
            f"Record the decision in compliance/DECISION_LOG.md and downgrade "
            f"`mek.toml > [compliance.gates] > {op}` to \"warn\" to proceed."
        )
        return 2

    # warn
    print(
        f"[compliance] warning: {op}. Is HITL approval recorded? "
        f"See compliance/HITL_TEMPLATE.md and compliance/DECISION_LOG.md."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
