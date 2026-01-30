"""Tests for the configuration settings."""

import os
import sys
from unittest.mock import patch

# Add src to path before importing app modules
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.insert(0, base_path)

from simple_krr_dashboard.config import Settings  # noqa: E402


def test_default_settings():
    """Test that default settings are correctly set."""
    settings = Settings()
    assert settings.APP_NAME == "Test Dashboard"
    assert settings.APP_VERSION == "1.0.0"
    assert settings.KUBERNETES_CLUSTER_NAME is None
    assert settings.KUBERNETES_DASHBOARD_CSV_PATH == "test.csv"
    assert settings.LOG_LEVEL == "INFO"
    expected_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    assert settings.LOG_FORMAT == expected_fmt


def test_settings_from_env():
    """Test that settings can be overridden by environment variables."""
    env_vars = {
        "APP_NAME": "Custom Dashboard",
        "APP_VERSION": "2.0.0",
        "KUBERNETES_CLUSTER_NAME": "test-cluster",
        "KUBERNETES_DASHBOARD_CSV_PATH": "/custom/path/test.csv",
        "LOG_LEVEL": "DEBUG",
        "LOG_FORMAT": "%(levelname)s - %(message)s",
    }
    with patch.dict(os.environ, env_vars):
        settings = Settings()
        assert settings.APP_NAME == "Custom Dashboard"
        assert settings.APP_VERSION == "2.0.0"
        assert settings.KUBERNETES_CLUSTER_NAME == "test-cluster"
        csv_path = "/custom/path/test.csv"
        assert settings.KUBERNETES_DASHBOARD_CSV_PATH == csv_path
        assert settings.LOG_LEVEL == "DEBUG"
        assert settings.LOG_FORMAT == "%(levelname)s - %(message)s"


def test_settings_case_sensitive():
    """Test that settings are case sensitive."""
    with patch.dict(os.environ, {"app_name": "lowercase"}):
        settings = Settings()
        # Should not be overridden
        assert settings.APP_NAME == "Test Dashboard"


def test_app_root_default():
    """Test that APP_ROOT defaults to /."""
    settings = Settings()
    assert settings.APP_ROOT == "/"


def test_app_root_from_env():
    """Test that APP_ROOT can be set via environment variable."""
    with patch.dict(os.environ, {"APP_ROOT": "/dashboard"}):
        settings = Settings()
        assert settings.APP_ROOT == "/dashboard"


def test_app_root_case_sensitive():
    """Test that APP_ROOT is case sensitive."""
    with patch.dict(os.environ, {"app_root": "/lowercase"}):
        settings = Settings()
        assert settings.APP_ROOT == "/"
