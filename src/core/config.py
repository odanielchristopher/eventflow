from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = Field(default="development", alias="APP_ENV")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=3000, alias="APP_PORT")
    mongodb_url: str = Field(default="mongodb://localhost:27017", alias="MONGODB_URL")
    mongodb_database: str = Field(default="eventflow", alias="MONGODB_DATABASE")
    minio_endpoint: str = Field(default="http://localhost:9000", alias="MINIO_ENDPOINT")
    minio_public_endpoint: str | None = Field(default=None, alias="MINIO_PUBLIC_ENDPOINT")
    minio_access_key: str = Field(default="eventflow", alias="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field(default="eventflow-secret", alias="MINIO_SECRET_KEY")
    minio_bucket: str = Field(default="eventflow-documents", alias="MINIO_BUCKET")
    minio_secure: bool = Field(default=False, alias="MINIO_SECURE")

    upload_dir: Path = Field(default=Path("./uploads"), alias="UPLOAD_DIR")

    @property
    def resolved_upload_dir(self) -> Path:
        return (BASE_DIR / self.upload_dir).resolve()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
