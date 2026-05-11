"""Classifies a Claude Code tool invocation into a risky-op category."""
from __future__ import annotations

import re

RM_RF_RE = re.compile(r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f|\brm\s+-[a-zA-Z]*f[a-zA-Z]*r")
FORCE_PUSH_RE = re.compile(
    r"\bgit\s+push\s+(--force(-with-lease)?|-f)\s+\S+\s+(main|master)"
)
DEPLOY_RE = re.compile(
    r"\b(kubectl\s+apply|docker\s+compose\s+up|terraform\s+apply|gcloud\s+run\s+deploy|aws\s+deploy)"
)
SCHEMA_FILE_RE = re.compile(r"(^|/)migrations/")
MONEY_SQL_RE = re.compile(r"\b(INSERT|UPDATE|DELETE)\b.*\b(accounts|journal|ledger|amount|balance|debit|credit)\b", re.IGNORECASE)
# `gh repo edit <repo> --visibility public|internal` — effectively irreversible due to
# search-index/Wayback caching. `--visibility private` is the safe direction; not flagged.
REPO_VISIBILITY_FLIP_RE = re.compile(
    r"\bgh\s+repo\s+edit\b[^\n]*\s--visibility\s+(public|internal)\b"
)


def classify_risky_op(tool_name: str, tool_input: dict) -> str | None:
    """Return one of the risky-op IDs, or None if the op is safe."""
    if tool_name == "Bash":
        cmd = (tool_input or {}).get("command", "")
        if RM_RF_RE.search(cmd):
            return "rm_rf"
        if FORCE_PUSH_RE.search(cmd):
            return "force_push_main"
        if DEPLOY_RE.search(cmd):
            return "deploy"
        if REPO_VISIBILITY_FLIP_RE.search(cmd):
            return "repo_visibility_flip"
        return None

    if tool_name in ("Edit", "Write", "MultiEdit"):
        path = (tool_input or {}).get("file_path", "")
        text = (tool_input or {}).get("new_string") or (tool_input or {}).get("content", "")
        if SCHEMA_FILE_RE.search(path):
            return "schema_migration"
        if MONEY_SQL_RE.search(text):
            return "money_write"
        return None

    return None
