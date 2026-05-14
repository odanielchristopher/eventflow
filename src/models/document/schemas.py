from __future__ import annotations

from datetime import datetime

from sqlmodel import Field, SQLModel

class DocumentBase(SQLModel):
    original_filename: str = Field(max_length=255)
    content_type: str = Field(max_length=255)
    extension: str = Field(max_length=20)
    size_bytes: int = Field(ge=0)

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(SQLModel):
    original_filename: str | None = Field(default=None, max_length=255)
    content_type: str | None = Field(default=None, max_length=255)
    extension: str | None = Field(default=None, max_length=20)
    size_bytes: int | None = Field(default=None, ge=0)

class DocumentRead(DocumentBase):
    id: int
    created_at: datetime
