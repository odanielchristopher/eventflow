from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url

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
    sql_echo: bool = Field(default=True, alias="SQL_ECHO")

    database_url: str = Field(
        default="sqlite+aiosqlite:///./sqlite_data/eventflow.db",
        alias="DATABASE_URL",
    )
    sqlite_database_url: str = Field(
        default="sqlite+aiosqlite:///./sqlite_data/eventflow.db",
        alias="SQLITE_DATABASE_URL",
    )
    postgres_database_url: str = Field(
        default="postgresql+asyncpg://eventflow:eventflow@localhost:5432/eventflow",
        alias="POSTGRES_DATABASE_URL",
    )

    upload_dir: Path = Field(default=Path("./uploads"), alias="UPLOAD_DIR")

    @property
    def resolved_upload_dir(self) -> Path:
        return (BASE_DIR / self.upload_dir).resolve()

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")

    @property
    def is_postgres(self) -> bool:
        return self.database_url.startswith("postgresql")

    @property
    def resolved_sqlite_database_path(self) -> Path | None:
        if not self.is_sqlite:
            return None

        database = make_url(self.database_url).database
        if database is None or database == ":memory:":
            return None

        return (BASE_DIR / database).resolve()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
