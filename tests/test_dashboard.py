"""Tests for the dashboard application."""

import json
import os
import sys
from unittest.mock import patch

import pytest

# Add src to path before importing app modules
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.insert(0, base_path)

from flask import Flask  # noqa: E402

from simple_krr_dashboard.main import create_app  # noqa: E402


@pytest.fixture
def app():
    """Create a test Flask application."""
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return [
        {"namespace": "default", "pod": "pod1", "status": "GOOD"},
        {"namespace": "kube-system", "pod": "pod2", "status": "WARNING"},
    ]


def test_index_route(client, sample_data):
    """Test the index route."""
    mock_path = "simple_krr_dashboard.main.create_deployment_data"
    with patch(mock_path, return_value=sample_data):
        response = client.get("/")
        assert response.status_code == 200


def test_get_data_route(client, sample_data):
    """Test the /api/data route."""
    mock_path = "simple_krr_dashboard.main.create_deployment_data"
    with patch(mock_path, return_value=sample_data):
        response = client.get("/api/data")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["namespace"] == "default"
        assert data[1]["namespace"] == "kube-system"


def test_get_data_route_error(client):
    """Test the /api/data route handles errors gracefully."""
    with patch(
        "simple_krr_dashboard.main.create_deployment_data",
        side_effect=Exception("Test error"),
    ):
        response = client.get("/api/data")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0


def test_toggle_theme_route(client):
    """Test the theme toggle functionality."""
    # Test switching from dark to light
    response = client.post(
        "/api/theme",
        json={"theme": "dark"},
        content_type="application/json",
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["theme"] == "light"

    # Test switching from light to dark
    response = client.post(
        "/api/theme",
        json={"theme": "light"},
        content_type="application/json",
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["theme"] == "dark"


def test_toggle_theme_route_default(client):
    """Test the theme toggle functionality with default theme."""
    response = client.post(
        "/api/theme",
        json={},
        content_type="application/json",
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    # Default to light when theme is not provided
    assert data["theme"] == "light"


def test_main():
    """Test the main function."""
    create_app_path = "simple_krr_dashboard.main.create_app"
    with patch(create_app_path) as mock_create_app, patch(
        "flask.Flask.run"
    ) as mock_run:
        from simple_krr_dashboard.main import main

        app = Flask(__name__)
        mock_create_app.return_value = app
        main()
        mock_create_app.assert_called_once()
        expected_args = {"host": "0.0.0.0", "port": 8080, "debug": False}
        mock_run.assert_called_once_with(**expected_args)
