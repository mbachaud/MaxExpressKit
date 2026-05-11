"""PreToolUse hook: warn when float arithmetic touches money-shaped identifiers.

Reads a Claude Code hook payload from stdin. Writes a warning to stdout when
it detects a float literal assigned to (or operated on with) an identifier
matching the money patterns. Always exits 0 — warn-only by default.
"""
from __future__ import annotations

import json
import re
import sys

MONEY_IDENTIFIER_RE = re.compile(
    r"\b(amount|price|balance|total|cost|fee|tax|revenue|profit)_?\w*\b",
    re.IGNORECASE,
)
FLOAT_LITERAL_RE = re.compile(r"\b\d+\.\d+\b")


def has_float_money_issue(text: str) -> list[str]:
    """Return a list of money-shaped identifier names that appear on lines with float literals."""
    issues: list[str] = []
    for line in text.splitlines():
        # Skip Decimal(...) literals.
        if "Decimal(" in line:
            continue
        if FLOAT_LITERAL_RE.search(line):
            for m in MONEY_IDENTIFIER_RE.finditer(line):
                issues.append(m.group(0))
    return issues


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return 0

    tool = payload.get("tool_name", "")
    if tool not in ("Edit", "Write", "MultiEdit"):
        return 0

    inp = payload.get("tool_input", {}) or {}
    text = inp.get("new_string") or inp.get("content") or ""

    issues = has_float_money_issue(text)
    if not issues:
        return 0

    unique = sorted(set(issues))
    print(
        "[ledger] warning: float arithmetic detected on money-shaped identifier(s): "
        + ", ".join(unique)
        + ". Use lib.decimal_math helpers (to_decimal, sum_money, pct_of)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
