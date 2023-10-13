from typing import Any

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.constants import Environment


class Config(BaseSettings):
    DATABASE_URL: PostgresDsn

    SITE_DOMAIN: str = "jobhunter.com"

    ENVIRONMENT: Environment = Environment.PRODUCTION

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str]

    APP_VERSION: str = "1"

    model_config = SettingsConfigDict(extra="ignore")


settings = Config(_env_file=".env", extra="ignore")

app_configs: dict[str, Any] = {"title": "App API"}
if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
