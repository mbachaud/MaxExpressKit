"""Unit tests for lib/config.py."""
from pathlib import Path

from lib.config import DEFAULT_CONFIG, load_mek_toml


def test_no_file_returns_defaults(tmp_path: Path):
    cfg = load_mek_toml(tmp_path)
    assert cfg == DEFAULT_CONFIG


def test_partial_overrides_merge(tmp_path: Path):
    (tmp_path / "mek.toml").write_text(
        '[compliance.gates]\nrm_rf = "block"\n', encoding="utf-8"
    )
    cfg = load_mek_toml(tmp_path)
    assert cfg["compliance"]["gates"]["rm_rf"] == "block"
    # Other defaults remain.
    assert cfg["drift"]["divergence_threshold"] == 0.15


def test_invalid_toml_returns_defaults_silently(tmp_path: Path):
    (tmp_path / "mek.toml").write_text("not [valid toml", encoding="utf-8")
    cfg = load_mek_toml(tmp_path)
    assert cfg == DEFAULT_CONFIG


def test_walks_up_to_find_toml(tmp_path: Path):
    (tmp_path / "mek.toml").write_text(
        '[mek]\nstrictness = "block"\n', encoding="utf-8"
    )
    nested = tmp_path / "a" / "b" / "c"
    nested.mkdir(parents=True)
    cfg = load_mek_toml(nested)
    assert cfg["mek"]["strictness"] == "block"
