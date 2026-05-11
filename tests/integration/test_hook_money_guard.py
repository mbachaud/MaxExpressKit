"""Integration test for the money_math_guard PreToolUse hook."""
import json
import subprocess
import sys
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / "hooks" / "scripts" / "money_math_guard.py"


def _invoke(payload: dict) -> tuple[int, str]:
    """Run the hook with a JSON payload on stdin."""
    p = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=10,
    )
    return p.returncode, p.stderr + p.stdout


def test_float_assigned_to_money_identifier_warns():
    payload = {
        "tool_name": "Edit",
        "tool_input": {
            "file_path": "foo.py",
            "new_string": "amount_total = 33.33\n",
        },
    }
    code, output = _invoke(payload)
    assert code == 0, "warn-by-default never blocks"
    assert "float" in output.lower()
    assert "amount_total" in output


def test_decimal_assigned_to_money_identifier_is_silent():
    payload = {
        "tool_name": "Edit",
        "tool_input": {
            "file_path": "foo.py",
            "new_string": 'amount_total = Decimal("33.33")\n',
        },
    }
    code, output = _invoke(payload)
    assert code == 0
    assert output == ""


def test_float_on_non_money_identifier_is_silent():
    payload = {
        "tool_name": "Edit",
        "tool_input": {
            "file_path": "foo.py",
            "new_string": "ratio = 0.5\n",
        },
    }
    code, output = _invoke(payload)
    assert code == 0
    assert output == ""


def test_non_edit_tool_is_silent():
    payload = {
        "tool_name": "Read",
        "tool_input": {"file_path": "foo.py"},
    }
    code, output = _invoke(payload)
    assert code == 0
    assert output == ""
