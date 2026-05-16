from __future__ import annotations

from datetime import time as time_type
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Time
from sqlmodel import Field, Relationship, SQLModel

from src.models.activity_speaker.entity import ActivitySpeaker

if TYPE_CHECKING:
    from src.models.event.entity import Event
    from src.models.speaker.entity import Speaker


class Activity(SQLModel, table=True):
    __tablename__ = "activities"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(String(length=255), nullable=False))
    scheduled_at: time_type = Field(sa_column=Column(Time(), nullable=False))
    event_id: int = Field(foreign_key="events.id", nullable=False)

    event: "Event" = Relationship(back_populates="activities")
    speakers: list["Speaker"] = Relationship(
        back_populates="activities",
        link_model=ActivitySpeaker,
    )
