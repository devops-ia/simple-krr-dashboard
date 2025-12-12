"""Configuration settings for the Simple KRR Dashboard."""

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    # Application settings
    APP_NAME: str = "Simple KRR Dashboard"
    APP_VERSION: str = "1.0.0"

    # Kubernetes settings
    KUBERNETES_CLUSTER_NAME: str | None = None
    KUBERNETES_DASHBOARD_CSV_PATH: str = "/reports/report.table.csv"

    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_OUTPUT_FORMAT: str = "logfmt"  # text, logfmt and json
    DISABLE_HTTP_LOGS: bool = False


settings = Settings()
