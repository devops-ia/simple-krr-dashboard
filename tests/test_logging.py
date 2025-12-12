"""Tests for the logging utilities."""

import logging
import os
import sys
from unittest.mock import patch

import pytest

# Add src to path before importing app modules
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.insert(0, base_path)

from simple_krr_dashboard.utils.logging import (  # noqa: E402
    JsonFormatter,
    LogfmtFormatter,
    get_formatter,
    get_logger,
    setup_logging,
)


def test_get_logger():
    """Test that get_logger returns a proper logger instance."""
    logger = get_logger(__name__)
    assert isinstance(logger, logging.Logger)
    assert logger.name == __name__


def test_setup_logging_default_values():
    """Test setup_logging with default values."""
    with patch("logging.basicConfig") as mock_config:
        setup_logging()
        mock_config.assert_called_once()
        args, kwargs = mock_config.call_args
        assert kwargs["level"] == "INFO"
        assert "handlers" in kwargs
        assert len(kwargs["handlers"]) == 1


def test_setup_logging_custom_values():
    """Test setup_logging with custom values."""
    with patch("logging.basicConfig") as mock_config:
        setup_logging(level="DEBUG", output_format="json")
        mock_config.assert_called_once()
        args, kwargs = mock_config.call_args
        assert kwargs["level"] == "DEBUG"
        assert "handlers" in kwargs


def test_setup_logging_invalid_level():
    """Test setup_logging with an invalid logging level."""
    with patch("logging.basicConfig") as mock_config:
        mock_config.side_effect = ValueError("Invalid log level")
        with pytest.raises(ValueError):
            setup_logging(level="INVALID_LEVEL")


def test_get_formatter_text():
    """Test get_formatter returns correct formatter for text format."""
    formatter = get_formatter("text")
    assert isinstance(formatter, logging.Formatter)
    assert not isinstance(formatter, (LogfmtFormatter, JsonFormatter))


def test_get_formatter_logfmt():
    """Test get_formatter returns LogfmtFormatter for logfmt format."""
    formatter = get_formatter("logfmt")
    assert isinstance(formatter, LogfmtFormatter)


def test_get_formatter_json():
    """Test get_formatter returns JsonFormatter for json format."""
    formatter = get_formatter("json")
    assert isinstance(formatter, JsonFormatter)


def test_logfmt_formatter():
    """Test LogfmtFormatter formats log records correctly."""
    formatter = LogfmtFormatter()
    record = logging.LogRecord(
        name="test.logger",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    output = formatter.format(record)
    assert "level=info" in output
    assert "logger=test.logger" in output
    assert 'msg="Test message"' in output
    assert "time=" in output


def test_json_formatter():
    """Test JsonFormatter formats log records correctly."""
    import json

    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test.logger",
        level=logging.WARNING,
        pathname="",
        lineno=0,
        msg="Test warning",
        args=(),
        exc_info=None,
    )
    output = formatter.format(record)
    log_data = json.loads(output)
    assert log_data["level"] == "warning"
    assert log_data["logger"] == "test.logger"
    assert log_data["message"] == "Test warning"
    assert "time" in log_data
