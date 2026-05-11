"""Integration test for the post_task_drift hook."""
import json
import subprocess
import sys
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / "hooks" / "scripts" / "post_task_drift.py"


def _invoke(cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input="{}",
        capture_output=True,
        text=True,
        timeout=30,
        cwd=str(cwd),
    )


def test_no_baseline_is_silent(tmp_path: Path):
    p = _invoke(tmp_path)
    assert p.returncode == 0
    assert p.stdout == ""


def test_baseline_with_divergence_prints(tmp_path: Path):
    mek_dir = tmp_path / ".mek"
    mek_dir.mkdir()
    (mek_dir / "drift-baseline.json").write_text(
        json.dumps({
            "schema_version": "1.0",
            "updated_at": "2026-05-10T00:00:00Z",
            "preset": "python",
            "dimensions": {
                "security": {"auto": 0.5, "manual": "A+", "confidence": 0.9, "floor": None},
            },
        }),
        encoding="utf-8",
    )
    p = _invoke(tmp_path)
    assert p.returncode == 0
    assert "security" in p.stdout
    assert "divergence" in p.stdout.lower()


def test_baseline_aligned_is_silent(tmp_path: Path):
    mek_dir = tmp_path / ".mek"
    mek_dir.mkdir()
    (mek_dir / "drift-baseline.json").write_text(
        json.dumps({
            "schema_version": "1.0",
            "updated_at": "2026-05-10T00:00:00Z",
            "preset": "python",
            "dimensions": {
                "security": {"auto": 0.95, "manual": "A+", "confidence": 0.9, "floor": None},
            },
        }),
        encoding="utf-8",
    )
    p = _invoke(tmp_path)
    assert p.returncode == 0
    assert p.stdout == ""
