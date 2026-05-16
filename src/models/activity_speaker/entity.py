from __future__ import annotations

from sqlmodel import Field, SQLModel


class ActivitySpeaker(SQLModel, table=True):
    __tablename__ = "activity_speakers"

    activity_id: int = Field(
        foreign_key="activities.id",
        primary_key=True,
        nullable=False,
    )
    speaker_id: int = Field(
        foreign_key="speakers.id",
        primary_key=True,
        nullable=False,
    )
