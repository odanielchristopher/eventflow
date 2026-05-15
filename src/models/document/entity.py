from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.event.entity import Event

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class Document(SQLModel, table=True):
    __tablename__ = "documents"

    id: int | None = Field(default=None, primary_key=True)
    original_filename: str = Field(max_length=255, nullable=False)
    content_type: str = Field(max_length=255, nullable=False)
    extension: str = Field(max_length=20, nullable=False)
    size_bytes: int = Field(nullable=False, ge=0)
    event_id: int | None = Field(default=None, foreign_key="events.id", nullable=True)
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    event: Optional["Event"] = Relationship(back_populates="documents")
