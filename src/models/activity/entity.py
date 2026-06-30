from __future__ import annotations

from datetime import time as time_type

from beanie import Document
from pydantic import Field, field_validator
from pymongo import IndexModel


class Activity(Document):
    title: str = Field(max_length=255)
    scheduled_at: time_type
    event_id: str
    speaker_ids: list[str] = Field(min_length=1)

    @field_validator("scheduled_at", mode="before")
    @classmethod
    def parse_scheduled_at(cls, value):
        if isinstance(value, str):
            return time_type.fromisoformat(value)
        return value

    class Settings:
        name = "activities"
        indexes = [
            IndexModel([("event_id", 1), ("scheduled_at", 1), ("_id", 1)]),
            IndexModel([("title", 1)]),
            IndexModel([("speaker_ids", 1)]),
        ]
        bson_encoders = {
            time_type: lambda value: value.isoformat(),
        }
