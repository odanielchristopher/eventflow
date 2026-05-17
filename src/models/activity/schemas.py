from __future__ import annotations

from datetime import time as time_type

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel

from src.models.speaker import SpeakerRead


class ActivityBase(SQLModel):
    title: str = Field(max_length=255)
    scheduled_at: time_type
    event_id: int


class ActivityCreate(ActivityBase):
    speaker_ids: list[int] = Field(min_length=1)


class ActivityUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=255)
    scheduled_at: time_type | None = None
    event_id: int | None = None
    speaker_ids: list[int] | None = Field(default=None, min_length=1)


class ActivityRead(ActivityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    speakers: list[SpeakerRead] = Field(default_factory=list)
