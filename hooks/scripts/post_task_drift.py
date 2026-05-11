"""Stop hook: if a baseline exists, compute current scores and report divergences."""
from __future__ import annotations

import os
import sys
from pathlib import Path

PLUGIN_ROOT = Path(os.environ.get("CLAUDE_PLUGIN_ROOT", Path(__file__).resolve().parents[2]))
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from lib.config import load_mek_toml
from lib.drift_scoring.baseline import find_divergences, load_baseline


def main() -> int:
    cwd = Path.cwd()
    cfg = load_mek_toml(cwd)
    drift_cfg = cfg.get("drift", {})

    if not drift_cfg.get("auto_run_on_stop", True):
        return 0

    baseline = load_baseline(cwd)
    if baseline is None:
        return 0  # no baseline → nothing to compare

    divs = find_divergences(
        baseline,
        threshold=float(drift_cfg.get("divergence_threshold", 0.15)),
        min_confidence=float(drift_cfg.get("min_confidence", 0.5)),
    )
    if not divs:
        return 0

    print("[drift] divergences detected:")
    for d in divs:
        if d.reason == "floor":
            print(f"  - {d.dimension}: auto={d.auto:.2f} below floor")
        else:
            print(
                f"  - {d.dimension}: auto={d.auto:.2f} vs manual={d.manual:.2f} "
                f"(delta={d.delta:.2f}, conf={d.confidence:.2f})"
            )
    print("Run `/mek-drift` for details or `/mek-drift accept` to update baseline.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
