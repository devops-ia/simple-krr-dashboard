"""Test configuration and fixtures for the Simple KRR Dashboard."""

import os
import sys
from unittest.mock import patch

import pytest

# Add src to path before importing app modules
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.insert(0, base_path)

from simple_krr_dashboard.main import create_app  # noqa: E402


@pytest.fixture(autouse=True)
def mock_env():
    """Mock environment variables for testing."""
    env_vars = {
        "APP_NAME": "Test Dashboard",
        "DEBUG": "false",
        "LOG_LEVEL": "INFO",
        "CACHE_ENABLED": "true",
        "CACHE_TTL": "300",
        "KUBERNETES_DASHBOARD_CSV_PATH": "test.csv",
    }
    with patch.dict(os.environ, env_vars):
        yield env_vars


@pytest.fixture
def mock_streamlit():
    """Mock Streamlit functions for testing."""
    with patch("streamlit.title"), patch("streamlit.container"), patch(
        "streamlit.metric"
    ), patch("streamlit.bar_chart"), patch("streamlit.line_chart"), patch(
        "streamlit.dataframe"
    ):
        yield


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "KUBERNETES_CLUSTER_NAME": "test-cluster",
            "KUBERNETES_DASHBOARD_CSV_PATH": "/test/path/report.table.csv",
        }
    )
    return app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the app."""
    return app.test_cli_runner()
