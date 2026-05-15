from __future__ import annotations

from datetime import datetime

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel

class DocumentBase(SQLModel):
    original_filename: str = Field(max_length=255)
    content_type: str = Field(max_length=255)
    extension: str = Field(max_length=20)
    size_bytes: int = Field(ge=0)

class DocumentCreate(DocumentBase):
    event_id: int | None = None

class DocumentUpdate(SQLModel):
    original_filename: str | None = Field(default=None, max_length=255)
    content_type: str | None = Field(default=None, max_length=255)
    extension: str | None = Field(default=None, max_length=20)
    size_bytes: int | None = Field(default=None, ge=0)
    event_id: int | None = None

class DocumentRead(DocumentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int | None = None
    created_at: datetime
