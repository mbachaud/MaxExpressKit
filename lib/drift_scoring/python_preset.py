"""Auto-scorers for Python projects. Returns dimension dict ready for baseline."""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def _run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    p = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=300,
        creationflags=CREATE_NO_WINDOW,
    )
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def score_test_pass_rate(project_root: Path) -> tuple[float, float]:
    code, out = _run(
        ["python", "-m", "pytest", "--no-header", "-q", "--tb=no"], project_root
    )
    # Look for "N passed, M failed" pattern.
    import re
    m = re.search(r"(\d+) passed", out)
    f = re.search(r"(\d+) failed", out)
    passed = int(m.group(1)) if m else 0
    failed = int(f.group(1)) if f else 0
    if passed + failed == 0:
        return 0.0, 0.0  # no tests, no confidence
    return passed / (passed + failed), 1.0


def score_lint(project_root: Path) -> tuple[float, float]:
    code, out = _run(["ruff", "check", "."], project_root)
    if code == 0:
        return 1.0, 1.0
    import re
    m = re.search(r"Found (\d+) error", out)
    errors = int(m.group(1)) if m else 1
    # Heuristic: 0 errors = 1.0, 100+ errors = 0.0, linear in between.
    score = max(0.0, 1.0 - errors / 100.0)
    return score, 1.0


def score_coverage(project_root: Path) -> tuple[float, float]:
    code, out = _run(
        ["python", "-m", "pytest", "--cov=.", "--cov-report=json", "-q"], project_root
    )
    cov_file = project_root / "coverage.json"
    if not cov_file.is_file():
        return 0.0, 0.5
    try:
        data = json.loads(cov_file.read_text(encoding="utf-8"))
        pct = float(data.get("totals", {}).get("percent_covered", 0.0)) / 100.0
        return pct, 0.9
    except (json.JSONDecodeError, OSError):
        return 0.0, 0.5


def score_all(project_root: Path) -> dict:
    """Return a dimensions dict ready to drop into a baseline."""
    pass_rate, c1 = score_test_pass_rate(project_root)
    lint, c2 = score_lint(project_root)
    coverage, c3 = score_coverage(project_root)
    return {
        "test_pass_rate": {"auto": pass_rate, "manual": None, "confidence": c1, "floor": 0.85},
        "lint_score":     {"auto": lint,      "manual": None, "confidence": c2, "floor": 0.95},
        "coverage":       {"auto": coverage,  "manual": None, "confidence": c3, "floor": 0.70},
        "security":       {"auto": 0.0,       "manual": None, "confidence": 0.0, "floor": None},
    }
