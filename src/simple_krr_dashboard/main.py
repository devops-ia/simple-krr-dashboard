"""Main dashboard application for Kubernetes monitoring."""

import logging

from flask import Flask, jsonify, render_template, request

from simple_krr_dashboard.config import settings
from simple_krr_dashboard.data.sample_data import create_deployment_data
from simple_krr_dashboard.utils.logging import get_logger

logger = get_logger(__name__)


class ThemeRequestFilter(logging.Filter):
    """Filter to exclude theme-related API requests from logging."""

    def filter(self, record):
        """Filter out theme-related API requests from the log records.

        Args:
            record: The log record to be filtered

        Returns:
            bool: True if the record should be logged, False otherwise
        """
        return "/api/theme" not in record.getMessage()


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Configure werkzeug logger for HTTP requests
    werkzeug_logger = logging.getLogger("werkzeug")
    if settings.DISABLE_HTTP_LOGS:
        werkzeug_logger.setLevel(logging.ERROR)
    else:
        # Add filter to exclude theme-related API requests
        for handler in werkzeug_logger.handlers:
            handler.addFilter(ThemeRequestFilter())

    app.config.update(
        APP_NAME=settings.APP_NAME,
        APP_VERSION=settings.APP_VERSION,
        KUBERNETES_CLUSTER_NAME=settings.KUBERNETES_CLUSTER_NAME,
        KUBERNETES_DASHBOARD_CSV_PATH=settings.KUBERNETES_DASHBOARD_CSV_PATH,
        LOG_LEVEL=settings.LOG_LEVEL,
        LOG_FORMAT=settings.LOG_FORMAT,
        CONTEXT_ROOT=settings.CONTEXT_ROOT,
    )

    @app.route(settings.CONTEXT_ROOT)
    def index():
        """Render the main dashboard page."""
        return render_template(
            "index.html",
            app_name=settings.APP_NAME,
            app_version=settings.APP_VERSION,
            kubernetes_cluster_name=settings.KUBERNETES_CLUSTER_NAME,
            theme="dark",
        )

    @app.route(settings.CONTEXT_ROOT.rstrip("/") + "/api/data")
    def get_data():
        """Get deployment data from the system."""
        try:
            data = create_deployment_data()
            for row in data:
                for key in row:
                    if row[key] is None:
                        row[key] = ""
            return jsonify(data)
        except Exception as e:
            logger.error(f"Error getting deployment data: {str(e)}")
            return jsonify([])

    @app.route(settings.CONTEXT_ROOT.rstrip("/") + "/api/theme", methods=["POST"])
    def toggle_theme():
        """Toggle between light and dark theme."""
        current_theme = request.json.get("theme", "dark")
        new_theme = "light" if current_theme == "dark" else "dark"
        return jsonify({"theme": new_theme})

    return app


def main():
    """Run the Flask application server."""
    app = create_app()

    # Disable werkzeug HTTP logs if configured
    if settings.DISABLE_HTTP_LOGS:
        log = logging.getLogger("werkzeug")
        log.setLevel(logging.ERROR)

    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    main()
