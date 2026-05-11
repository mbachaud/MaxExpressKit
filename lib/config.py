"""Load and merge mek.toml configuration."""
from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover
    import tomli as tomllib

DEFAULT_CONFIG: dict[str, Any] = {
    "mek": {"version": "0.1.0", "strictness": "warn"},
    "compliance": {
        "templates_dir": "compliance",
        "risky_ops_file": "compliance/RISKY_OPS.yaml",
        "staleness_days": 90,
        "gates": {
            "rm_rf": "warn",
            "deploy": "warn",
            "money_write": "warn",
            "schema_migration": "warn",
            "force_push_main": "warn",
        },
    },
    "drift": {
        "baseline_file": ".mek/drift-baseline.json",
        "preset": "python",
        "divergence_threshold": 0.15,
        "min_confidence": 0.5,
        "auto_run_on_stop": True,
    },
    "ledger": {
        "money_identifier_patterns": [
            "amount_*",
            "price_*",
            "balance_*",
            "total_*",
            "cost_*",
        ],
        "warn_on_float": True,
    },
    "source_apps": {
        "scorerift_path": "auto",
        "bookkeeper_path": "auto",
        "cosmictasha_url": "auto",
    },
}


def _deep_merge(base: dict, override: dict) -> dict:
    out = deepcopy(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def _find_toml(start: Path) -> Path | None:
    cur = start.resolve()
    for parent in [cur, *cur.parents]:
        candidate = parent / "mek.toml"
        if candidate.is_file():
            return candidate
    return None


def load_mek_toml(start: Path | str = ".") -> dict[str, Any]:
    """Load mek.toml walking up from `start`; return defaults if absent/invalid."""
    toml_path = _find_toml(Path(start))
    if toml_path is None:
        return deepcopy(DEFAULT_CONFIG)
    try:
        with toml_path.open("rb") as f:
            user = tomllib.load(f)
    except (tomllib.TOMLDecodeError, OSError):
        return deepcopy(DEFAULT_CONFIG)
    return _deep_merge(DEFAULT_CONFIG, user)
