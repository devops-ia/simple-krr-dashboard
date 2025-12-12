"""Logging configuration for the Simple KRR Dashboard."""

import json
import logging
import sys
from datetime import datetime

from simple_krr_dashboard.config import settings


class LogfmtFormatter(logging.Formatter):
    """Formatter for logfmt output format."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as logfmt.

        Args:
            record: Log record to format

        Returns:
            Formatted log message in logfmt format
        """
        timestamp = datetime.fromtimestamp(record.created).isoformat()
        pairs = [
            f"time={timestamp}",
            f"level={record.levelname.lower()}",
            f"logger={record.name}",
            f'msg="{record.getMessage()}"',
        ]

        # Add extra fields if present
        if hasattr(record, "extra"):
            for key, value in record.extra.items():
                pairs.append(f'{key}="{value}"')

        return " ".join(pairs)


class JsonFormatter(logging.Formatter):
    """Formatter for JSON output format."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON.

        Args:
            record: Log record to format

        Returns:
            Formatted log message in JSON format
        """
        log_data = {
            "time": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname.lower(),
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extra fields if present
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def get_formatter(output_format: str) -> logging.Formatter:
    """Get the appropriate formatter based on output format.

    Args:
        output_format: Output format (text, logfmt, json)

    Returns:
        logging.Formatter: Configured formatter
    """
    if output_format == "logfmt":
        return LogfmtFormatter()
    if output_format == "json":
        return JsonFormatter()
    # Default text format
    return logging.Formatter(settings.LOG_FORMAT)


def setup_logging(
    level: str | None = None,
    output_format: str | None = None,
) -> None:
    """Configure logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)  # noqa: E501
        output_format: Output format (text, logfmt, json)
    """
    level = level or settings.LOG_LEVEL
    output_format = output_format or settings.LOG_OUTPUT_FORMAT

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(get_formatter(output_format))

    logging.basicConfig(
        level=level,
        handlers=[handler],
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
