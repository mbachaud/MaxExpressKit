"""Unit tests for lib/source_app_detect.py."""
from unittest.mock import patch

from lib.source_app_detect import has_bookkeeper, has_cosmictasha, has_scorerift


@patch("lib.source_app_detect.shutil.which")
def test_has_scorerift_true_when_on_path(mock_which):
    mock_which.return_value = "/usr/local/bin/scorerift"
    assert has_scorerift() is True


@patch("lib.source_app_detect.shutil.which")
def test_has_scorerift_false_when_absent(mock_which):
    mock_which.return_value = None
    assert has_scorerift() is False


@patch("lib.source_app_detect.shutil.which")
def test_has_bookkeeper_true_when_on_path(mock_which):
    mock_which.return_value = "/usr/local/bin/bookkeeper"
    assert has_bookkeeper() is True


@patch("lib.source_app_detect.urllib.request.urlopen")
def test_has_cosmictasha_returns_dict(mock_urlopen):
    # Simulate a healthy CT response.
    class _Resp:
        def __enter__(self): return self
        def __exit__(self, *a): pass
        def read(self): return b'{"version": "0.1.0"}'
        status = 200
    mock_urlopen.return_value = _Resp()
    result = has_cosmictasha()
    assert result["present"] is True
    assert result["url"] == "http://localhost:3000/api/health"
    assert result["version"] == "0.1.0"


@patch("lib.source_app_detect.urllib.request.urlopen")
def test_has_cosmictasha_handles_error(mock_urlopen):
    mock_urlopen.side_effect = OSError("connection refused")
    result = has_cosmictasha()
    assert result["present"] is False
    assert result["url"] is None
    assert result["version"] is None
