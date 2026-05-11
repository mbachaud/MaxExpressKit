"""Unit tests for lib/drift_scoring/grades.py."""
import pytest

from lib.drift_scoring.grades import float_to_grade, grade_to_float


@pytest.mark.parametrize(
    ("grade", "expected"),
    [
        ("A+", 0.97), ("A", 0.93), ("A-", 0.90),
        ("B+", 0.87), ("B", 0.83), ("B-", 0.80),
        ("C+", 0.77), ("C", 0.73), ("C-", 0.70),
        ("D", 0.65), ("F", 0.50),
    ],
)
def test_grade_to_float(grade, expected):
    assert grade_to_float(grade) == pytest.approx(expected, abs=1e-9)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0.97, "A+"), (0.93, "A"), (0.90, "A-"),
        (0.85, "B"), (0.50, "F"), (0.0, "F"),
    ],
)
def test_float_to_grade(value, expected):
    assert float_to_grade(value) == expected


def test_unknown_grade_raises():
    with pytest.raises(ValueError):
        grade_to_float("Z+")
