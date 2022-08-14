import secrets
from typing import Any, Optional

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_HOST: AnyHttpUrl
    SERVER_PORT: int
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    PROJECT_NAME: str = "Cashback Calculator"

    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=str(values.get("POSTGRES_PORT")) or "5432",
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    CASHBACK_SERVICE_URL: AnyHttpUrl
    CASHBACK_SERVICE_TOKEN: str

    class Config:
        case_sensitive = True


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
print(settings.SQLALCHEMY_DATABASE_URI)
