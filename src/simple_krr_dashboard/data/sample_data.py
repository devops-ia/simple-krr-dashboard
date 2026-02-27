"""Sample data for the simple-krr-dashboard."""

import os
import threading

from simple_krr_dashboard.components.table import read_csv_file
from simple_krr_dashboard.config import settings
from simple_krr_dashboard.utils.logging import get_logger

logger = get_logger(__name__)

_cache_lock = threading.Lock()
_cached_data: list[dict] = []


def load_csv_data():
    """Load and process the CSV data."""
    csv_path = settings.KUBERNETES_DASHBOARD_CSV_PATH

    if not os.path.isabs(csv_path):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root = os.path.dirname(os.path.dirname(current_dir))
        project_root = os.path.dirname(root)
        csv_path = os.path.join(project_root, csv_path)

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at {csv_path}")

    headers, rows = read_csv_file(csv_path)
    return rows


def create_deployment_data():
    """Create deployment data from CSV, with fallback to cached data on read failure."""
    try:
        data = load_csv_data()
        with _cache_lock:
            _cached_data[:] = data
        return data
    except Exception as e:
        logger.warning("Failed to load CSV data, returning cached data: %s", e)
        with _cache_lock:
            return list(_cached_data)
