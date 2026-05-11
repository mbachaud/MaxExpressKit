"""Unit tests for lib/compliance_templates/risky_op_patterns.py."""
import pytest

from lib.compliance_templates.risky_op_patterns import classify_risky_op


@pytest.mark.parametrize(
    ("tool_name", "tool_input", "expected_op"),
    [
        ("Bash", {"command": "rm -rf /some/dir"}, "rm_rf"),
        ("Bash", {"command": "git push --force origin main"}, "force_push_main"),
        ("Bash", {"command": "git push --force origin master"}, "force_push_main"),
        ("Bash", {"command": "kubectl apply -f deploy.yaml"}, "deploy"),
        ("Bash", {"command": "docker compose up -d"}, "deploy"),
        ("Edit", {"file_path": "migrations/0042_add_col.sql", "new_string": "..."}, "schema_migration"),
        ("Write", {"file_path": "migrations/0043.py", "content": "..."}, "schema_migration"),
        ("Edit", {"file_path": "src/ledger.py", "new_string": "INSERT INTO accounts ..."}, "money_write"),
        ("Bash", {"command": "gh repo edit owner/repo --visibility public"}, "repo_visibility_flip"),
        ("Bash", {"command": "gh repo edit owner/repo --visibility internal"}, "repo_visibility_flip"),
        ("Bash", {"command": "gh repo edit mbachaud/MaxExpressKit  --visibility public"}, "repo_visibility_flip"),
    ],
)
def test_classify_risky_op(tool_name, tool_input, expected_op):
    assert classify_risky_op(tool_name, tool_input) == expected_op


@pytest.mark.parametrize(
    ("tool_name", "tool_input"),
    [
        ("Bash", {"command": "ls"}),
        ("Bash", {"command": "git status"}),
        ("Edit", {"file_path": "README.md", "new_string": "hello"}),
        ("Read", {"file_path": "anything.py"}),
    ],
)
def test_safe_ops_classify_to_none(tool_name, tool_input):
    assert classify_risky_op(tool_name, tool_input) is None
