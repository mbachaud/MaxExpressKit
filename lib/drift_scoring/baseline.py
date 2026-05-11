"""Load, save, and analyze .mek/drift-baseline.json."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from lib.drift_scoring.grades import grade_to_float

BASELINE_REL_PATH = Path(".mek/drift-baseline.json")


@dataclass(frozen=True)
class Divergence:
    dimension: str
    auto: float
    manual: float | None
    confidence: float
    delta: float | None
    reason: str  # "delta" | "floor"


def load_baseline(project_root: Path) -> dict | None:
    path = project_root / BASELINE_REL_PATH
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_baseline(project_root: Path, baseline: dict) -> None:
    path = project_root / BASELINE_REL_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(baseline, indent=2), encoding="utf-8")


def _manual_to_float(manual) -> float | None:
    if manual is None:
        return None
    if isinstance(manual, (int, float)):
        return float(manual)
    return grade_to_float(manual)


def find_divergences(
    baseline: dict,
    *,
    threshold: float = 0.15,
    min_confidence: float = 0.5,
) -> list[Divergence]:
    out: list[Divergence] = []
    for name, dim in baseline.get("dimensions", {}).items():
        auto = float(dim.get("auto", 0.0))
        confidence = float(dim.get("confidence", 1.0))
        manual = _manual_to_float(dim.get("manual"))
        floor = dim.get("floor")

        # Floor check fires regardless of confidence.
        if floor is not None and auto < float(floor):
            out.append(
                Divergence(
                    dimension=name,
                    auto=auto,
                    manual=manual,
                    confidence=confidence,
                    delta=None,
                    reason="floor",
                )
            )
            continue

        if manual is None or confidence < min_confidence:
            continue
        delta = abs(auto - manual)
        if delta > threshold:
            out.append(
                Divergence(
                    dimension=name,
                    auto=auto,
                    manual=manual,
                    confidence=confidence,
                    delta=delta,
                    reason="delta",
                )
            )
    return out
