from functools import lru_cache
from pathlib import Path

from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _secret_or_value(value: str | None, file_path: str | None) -> str | None:
    if file_path:
        return Path(file_path).read_text(encoding="utf-8").strip()
    return value


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"
    project_name: str = "VAULTLINK"
    api_v1_prefix: str = "/api"
    backend_cors_origins: list[AnyHttpUrl] = Field(default_factory=list)

    database_url: str | None = None
    database_url_file: str | None = None
    redis_url: str | None = None
    redis_url_file: str | None = None

    jwt_secret: str | None = None
    jwt_secret_file: str | None = None
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/api/auth/google/callback"

    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    email_from: str = "no-reply@altiquum.local"

    alpha_vantage_api_key: str = ""
    news_api_key: str = ""
    sentry_dsn: str = ""
    rate_limit_per_minute: int = 60

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_cors(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @property
    def resolved_database_url(self) -> str:
        value = _secret_or_value(self.database_url, self.database_url_file)
        if not value:
            raise RuntimeError("DATABASE_URL is required")
        return value

    @property
    def resolved_redis_url(self) -> str:
        value = _secret_or_value(self.redis_url, self.redis_url_file)
        if not value:
            raise RuntimeError("REDIS_URL is required")
        return value

    @property
    def resolved_jwt_secret(self) -> str:
        value = _secret_or_value(self.jwt_secret, self.jwt_secret_file)
        if not value or len(value) < 32:
            raise RuntimeError("JWT_SECRET must be at least 32 characters")
        return value

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
