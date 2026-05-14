from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class Document(SQLModel, table=True):
    __tablename__ = "documents"

    id: int | None = Field(default=None, primary_key=True)
    original_filename: str = Field(max_length=255, nullable=False)
    content_type: str = Field(max_length=255, nullable=False)
    extension: str = Field(max_length=20, nullable=False)
    size_bytes: int = Field(nullable=False, ge=0)
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
