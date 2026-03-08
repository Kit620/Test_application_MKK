"""Настройки приложения из переменных окружения."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Конфигурация приложения."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    api_key: str = "test-organizations-api-key"
    api_key_header: str = "X-API-Key"

    database_url: str = "postgresql://postgres:postgres@localhost:5432/organizations_db"

    app_title: str = "Справочник организаций API"
    app_version: str = "1.0.0"


settings = Settings()
