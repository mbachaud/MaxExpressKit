"""Unit tests for lib/drift_scoring/baseline.py."""
import json
from pathlib import Path

from lib.drift_scoring.baseline import (
    Divergence,
    find_divergences,
    load_baseline,
    save_baseline,
)

SAMPLE = {
    "schema_version": "1.0",
    "updated_at": "2026-05-10T22:01:00Z",
    "preset": "python",
    "dimensions": {
        "test_pass_rate":  {"auto": 0.93, "manual": None, "confidence": 1.0, "floor": 0.85},
        "lint_score":      {"auto": 1.0,  "manual": None, "confidence": 1.0, "floor": 0.95},
        "coverage":        {"auto": 0.78, "manual": None, "confidence": 0.9, "floor": 0.70},
        "security":        {"auto": 0.85, "manual": "A+", "confidence": 0.8, "floor": None},
    },
}


def test_save_then_load_roundtrip(tmp_path: Path):
    save_baseline(tmp_path, SAMPLE)
    loaded = load_baseline(tmp_path)
    assert loaded == SAMPLE


def test_load_missing_returns_none(tmp_path: Path):
    assert load_baseline(tmp_path) is None


def test_find_divergences_flags_security(tmp_path: Path):
    # auto=0.85 vs manual A+=0.97 → |0.12| < 0.15 → NOT flagged.
    # Bump auto to 0.70 → |0.27| > 0.15 → flagged.
    sample = json.loads(json.dumps(SAMPLE))
    sample["dimensions"]["security"]["auto"] = 0.70
    divs = find_divergences(sample, threshold=0.15, min_confidence=0.5)
    assert any(d.dimension == "security" for d in divs)


def test_low_confidence_is_silent():
    sample = json.loads(json.dumps(SAMPLE))
    sample["dimensions"]["security"]["auto"] = 0.10
    sample["dimensions"]["security"]["confidence"] = 0.3
    divs = find_divergences(sample, threshold=0.15, min_confidence=0.5)
    assert not any(d.dimension == "security" for d in divs)


def test_floor_violation_flags_independently():
    sample = json.loads(json.dumps(SAMPLE))
    sample["dimensions"]["lint_score"]["auto"] = 0.80  # below floor 0.95
    divs = find_divergences(sample, threshold=0.15, min_confidence=0.5)
    assert any(d.dimension == "lint_score" and d.reason == "floor" for d in divs)


def test_divergence_carries_values():
    sample = json.loads(json.dumps(SAMPLE))
    sample["dimensions"]["security"]["auto"] = 0.70
    divs = find_divergences(sample, threshold=0.15, min_confidence=0.5)
    d = next(d for d in divs if d.dimension == "security")
    assert isinstance(d, Divergence)
    assert d.auto == 0.70
    assert d.manual == 0.97
