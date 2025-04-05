"""Sample data for the simple-krr-dashboard."""

import os

from simple_krr_dashboard.components.table import read_csv_file
from simple_krr_dashboard.config import settings


def load_csv_data():
    """Load and process the CSV data."""
    csv_path = settings.KUBERNETES_DASHBOARD_CSV_PATH

    if not os.path.isabs(csv_path):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        csv_path = os.path.join(project_root, csv_path)

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at {csv_path}")

    headers, rows = read_csv_file(csv_path)
    return rows


def create_deployment_data():
    """Create deployment data from CSV."""
    try:
        return load_csv_data()
    except FileNotFoundError:
        return []
