"""Configuration settings for the Simple KRR Dashboard."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application settings
    APP_NAME: str = "Simple KRR Dashboard"
    APP_VERSION: str = "1.0.0"

    # Kubernetes settings
    KUBERNETES_CLUSTER_NAME: str | None = None
    KUBERNETES_DASHBOARD_CSV_PATH: str = "/reports/report.table.csv"

    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        """Pydantic configuration settings."""

        env_file = ".env"
        case_sensitive = True


settings = Settings()
