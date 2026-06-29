from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DocumentBase(BaseModel):
    original_filename: str = Field(max_length=255)
    content_type: str = Field(max_length=255)
    extension: str = Field(max_length=20)
    size_bytes: int = Field(ge=0)


class DocumentCreate(DocumentBase):
    event_id: str | None = None


class DocumentUpdate(BaseModel):
    original_filename: str | None = Field(default=None, max_length=255)
    content_type: str | None = Field(default=None, max_length=255)
    extension: str | None = Field(default=None, max_length=20)
    size_bytes: int | None = Field(default=None, ge=0)
    event_id: str | None = None


class DocumentRead(DocumentBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    event_id: str | None = None
    created_at: datetime

    @field_validator("id", "event_id", mode="before")
    @classmethod
    def stringify_ids(cls, value):
        if value is None:
            return None
        return str(value)
