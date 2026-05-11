"""Detect whether the user has CosmicTasha / ScoreRift / BookKeeper installed."""
from __future__ import annotations

import json
import shutil
import urllib.request

CT_DEFAULT_URL = "http://localhost:3000/api/health"


def has_scorerift() -> bool:
    return shutil.which("scorerift") is not None


def has_bookkeeper() -> bool:
    return shutil.which("bookkeeper") is not None


def has_cosmictasha(url: str = CT_DEFAULT_URL) -> dict:
    """Probe CosmicTasha's health endpoint.

    Returns {"present": bool, "url": str|None, "version": str|None}.
    """
    try:
        with urllib.request.urlopen(url, timeout=2) as resp:
            body = resp.read().decode("utf-8")
            data = json.loads(body) if body else {}
            return {"present": True, "url": url, "version": data.get("version")}
    except (OSError, json.JSONDecodeError):
        return {"present": False, "url": None, "version": None}
