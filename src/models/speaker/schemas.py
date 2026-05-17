from __future__ import annotations

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class SpeakerBase(SQLModel):
    name: str = Field(max_length=255)
    specialty: str = Field(max_length=255)
    bio: str = Field(max_length=1000)


class SpeakerCreate(SpeakerBase):
    pass


class SpeakerUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    specialty: str | None = Field(default=None, max_length=255)
    bio: str | None = Field(default=None, max_length=1000)


class SpeakerRead(SpeakerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
