"""Tests for the data module."""

from unittest.mock import patch

import pytest

import simple_krr_dashboard.data.sample_data as sample_data_module
from simple_krr_dashboard.data.sample_data import create_deployment_data, load_csv_data


def test_load_csv_data_file_not_found():
    """Test loading data when file is not found."""
    with patch(
        "simple_krr_dashboard.config.settings.KUBERNETES_DASHBOARD_CSV_PATH",
        "nonexistent.csv",
    ):
        with pytest.raises(FileNotFoundError):
            load_csv_data()


def test_create_deployment_data_file_not_found():
    """Test creating deployment data when file is not found."""
    with patch(
        "simple_krr_dashboard.data.sample_data.load_csv_data",
        side_effect=FileNotFoundError,
    ):
        data = create_deployment_data()
        assert isinstance(data, list)
        assert len(data) == 0


def test_create_deployment_data_success():
    """Test creating deployment data successfully."""
    sample_data = [
        {"namespace": "default", "pod": "pod1", "status": "GOOD"},
        {"namespace": "kube-system", "pod": "pod2", "status": "WARNING"},
    ]

    mock_path = "simple_krr_dashboard.data.sample_data.load_csv_data"
    with patch(mock_path, return_value=sample_data):
        data = create_deployment_data()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["namespace"] == "default"
        assert data[1]["namespace"] == "kube-system"


def test_create_deployment_data_returns_cache_on_failure(monkeypatch):
    """Test that cached data is served when CSV read fails (e.g. during kubectl cp)."""
    cached = [{"namespace": "default", "pod": "pod1", "status": "GOOD"}]
    monkeypatch.setattr(sample_data_module, "_cached_data", cached)
    with patch(
        "simple_krr_dashboard.data.sample_data.load_csv_data",
        side_effect=Exception("file truncated during write"),
    ):
        data = create_deployment_data()
        assert data == cached
