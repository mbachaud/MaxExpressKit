"""Integration test: scaffold payload (the files /mek-init drops into a project)."""
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[2]
SCAFFOLD = PLUGIN_ROOT / "scaffold"


def test_scaffold_has_mek_toml():
    assert (SCAFFOLD / "mek.toml").is_file()


def test_scaffold_has_compliance_templates():
    assert (SCAFFOLD / "compliance" / "HITL_TEMPLATE.md").is_file()
    assert (SCAFFOLD / "compliance" / "DECISION_LOG.md").is_file()
    assert (SCAFFOLD / "compliance" / "RISKY_OPS.yaml").is_file()


def test_scaffold_mek_toml_parses():
    import sys
    if sys.version_info >= (3, 11):
        import tomllib
    else:
        import tomli as tomllib
    data = tomllib.loads((SCAFFOLD / "mek.toml").read_text(encoding="utf-8"))
    assert data["mek"]["strictness"] == "warn"
    assert data["compliance"]["staleness_days"] == 90
