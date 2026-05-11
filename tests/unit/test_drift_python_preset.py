"""Regression tests for the python drift preset's confidence honesty."""
from pathlib import Path

from lib.drift_scoring import python_preset


def _fake_run(out: str, code: int = 0):
    """Return a _run replacement that yields the given (code, out)."""
    def _run(cmd, cwd, merge_stderr=True):
        return code, out
    return _run


def test_score_lint_clean_returns_full_confidence(monkeypatch):
    monkeypatch.setattr(python_preset, "_run", _fake_run("All checks passed!\n"))
    assert python_preset.score_lint(Path(".")) == (1.0, 1.0)


def test_score_lint_with_errors_returns_full_confidence(monkeypatch):
    monkeypatch.setattr(python_preset, "_run", _fake_run("Found 3 errors.\n", code=1))
    score, confidence = python_preset.score_lint(Path("."))
    assert confidence == 1.0
    assert score == 0.97  # 1.0 - 3/100


def test_score_lint_missing_ruff_returns_unmeasured_sentinel(monkeypatch):
    # Subprocess failed to launch ruff: empty stdout, nonzero exit.
    monkeypatch.setattr(python_preset, "_run", _fake_run("", code=1))
    assert python_preset.score_lint(Path(".")) == (0.0, 0.0)


def test_score_lint_unparseable_output_returns_unmeasured_sentinel(monkeypatch):
    # Some future ruff version changes its output format — we'd rather report
    # "no data" than fabricate a 0.99 score.
    monkeypatch.setattr(
        python_preset, "_run", _fake_run("some unexpected output\n", code=1)
    )
    assert python_preset.score_lint(Path(".")) == (0.0, 0.0)
