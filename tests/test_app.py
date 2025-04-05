"""Tests for the Flask application."""

import json
import os
import sys
from unittest.mock import patch

import pytest
from flask import Flask

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from simple_krr_dashboard.main import create_app


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
    with patch(
        "simple_krr_dashboard.main.create_deployment_data", return_value=sample_data
    ):
        response = client.get("/")
        assert response.status_code == 200


def test_get_data_route(client, sample_data):
    """Test the /api/data route."""
    with patch(
        "simple_krr_dashboard.main.create_deployment_data", return_value=sample_data
    ):
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
    assert data["theme"] == "light"  # Default to light when theme is not provided


def test_invalid_theme_request(client):
    """Test handling of invalid theme toggle requests."""
    response = client.post(
        "/api/theme",
        json={},
        content_type="application/json",
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["theme"] == "light"  # Default to light when theme is not provided
