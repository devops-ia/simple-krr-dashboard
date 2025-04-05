"""Logging configuration for the Simple KRR Dashboard."""

import logging
import sys

from simple_krr_dashboard.config import settings


def setup_logging(level: str | None = None, format_string: str | None = None) -> None:
    """Configure logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)  # noqa: E501
        format_string: Custom format string for log messages
    """
    level = level or settings.LOG_LEVEL
    format_string = format_string or settings.LOG_FORMAT

    logging.basicConfig(
        level=level,
        format=format_string,
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    logger = logging.getLogger(__name__)
    logger.debug("Logging configured successfully")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name.

    Args:
        name: Name of the logger

    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)
