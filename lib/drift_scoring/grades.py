"""Letter grade <-> float mapping for drift scoring."""
from __future__ import annotations

# Ordered high to low so float_to_grade picks the highest matching grade.
_GRADE_TABLE: list[tuple[str, float]] = [
    ("A+", 0.97), ("A", 0.93), ("A-", 0.90),
    ("B+", 0.87), ("B", 0.83), ("B-", 0.80),
    ("C+", 0.77), ("C", 0.73), ("C-", 0.70),
    ("D",  0.65), ("F",  0.50),
]
_GRADE_MAP = {g: v for g, v in _GRADE_TABLE}


def grade_to_float(grade: str) -> float:
    """Return the canonical float for a letter grade. Raises on unknown."""
    try:
        return _GRADE_MAP[grade]
    except KeyError as e:
        raise ValueError(f"unknown grade: {grade!r}") from e


def float_to_grade(value: float) -> str:
    """Return the highest letter grade whose threshold is <= value."""
    for grade, threshold in _GRADE_TABLE:
        if value >= threshold:
            return grade
    return "F"
