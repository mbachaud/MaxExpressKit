"""Shared fixtures across MEK tests."""
import sys
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parent.parent

# Make plugin root importable for all tests (lib/, hooks/).
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))


@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    """A clean tmp dir to use as a fake project root."""
    return tmp_path
