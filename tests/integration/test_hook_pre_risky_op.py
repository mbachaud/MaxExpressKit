"""Integration test for the pre_risky_op hook (warn-only by default)."""
import json
import subprocess
import sys
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / "hooks" / "scripts" / "pre_risky_op.py"


def _invoke(payload: dict, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=10,
        cwd=str(cwd) if cwd else None,
    )


def test_rm_rf_warns_without_blocking(tmp_path):
    p = _invoke(
        {"tool_name": "Bash", "tool_input": {"command": "rm -rf /tmp/x"}},
        cwd=tmp_path,
    )
    assert p.returncode == 0
    assert "rm_rf" in (p.stdout + p.stderr)
    assert "HITL" in (p.stdout + p.stderr)


def test_block_when_mek_toml_escalates(tmp_path):
    (tmp_path / "mek.toml").write_text(
        '[compliance.gates]\nrm_rf = "block"\n', encoding="utf-8"
    )
    p = _invoke(
        {"tool_name": "Bash", "tool_input": {"command": "rm -rf /tmp/x"}},
        cwd=tmp_path,
    )
    assert p.returncode == 2  # Claude Code convention: non-zero blocks
    assert "blocked" in (p.stdout + p.stderr).lower()


def test_safe_op_is_silent(tmp_path):
    p = _invoke(
        {"tool_name": "Bash", "tool_input": {"command": "ls"}},
        cwd=tmp_path,
    )
    assert p.returncode == 0
    assert p.stdout == ""


def test_off_strictness_suppresses_warning(tmp_path):
    (tmp_path / "mek.toml").write_text(
        '[compliance.gates]\nrm_rf = "off"\n', encoding="utf-8"
    )
    p = _invoke(
        {"tool_name": "Bash", "tool_input": {"command": "rm -rf /tmp/x"}},
        cwd=tmp_path,
    )
    assert p.returncode == 0
    assert p.stdout == ""
