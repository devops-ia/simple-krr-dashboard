"""Tests for the logging utilities."""

import logging
import os
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from simple_krr_dashboard.utils.logging import get_logger, setup_logging


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
        assert "%(asctime)s" in kwargs["format"]


def test_setup_logging_custom_values():
    """Test setup_logging with custom values."""
    with patch("logging.basicConfig") as mock_config:
        setup_logging(level="DEBUG", format_string="%(levelname)s - %(message)s")
        mock_config.assert_called_once()
        args, kwargs = mock_config.call_args
        assert kwargs["level"] == "DEBUG"
        assert kwargs["format"] == "%(levelname)s - %(message)s"


def test_setup_logging_invalid_level():
    """Test setup_logging with an invalid logging level."""
    with patch("logging.basicConfig") as mock_config:
        mock_config.side_effect = ValueError("Invalid log level")
        with pytest.raises(ValueError):
            setup_logging(level="INVALID_LEVEL")
