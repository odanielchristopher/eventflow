from __future__ import annotations

from datetime import time as time_type

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.models.speaker import SpeakerRead


class ActivityBase(BaseModel):
    title: str = Field(max_length=255)
    scheduled_at: time_type


class ActivityCreate(ActivityBase):
    speaker_ids: list[str] = Field(min_length=1)


class ActivityUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    scheduled_at: time_type | None = None
    speaker_ids: list[str] | None = Field(default=None, min_length=1)


class ActivityRead(ActivityBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    event_id: str = Field(exclude=True)
    speaker_ids: list[str] = Field(default_factory=list, exclude=True)
    speakers: list[SpeakerRead] = Field(default_factory=list)

    @field_validator("id", "event_id", mode="before")
    @classmethod
    def stringify_ids(cls, value) -> str:
        return str(value)
