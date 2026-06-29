from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SpeakerBase(BaseModel):
    name: str = Field(max_length=255)
    specialty: str = Field(max_length=255)
    bio: str = Field(max_length=1000)


class SpeakerCreate(SpeakerBase):
    pass


class SpeakerUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    specialty: str | None = Field(default=None, max_length=255)
    bio: str | None = Field(default=None, max_length=1000)


class SpeakerRead(SpeakerBase):
    model_config = ConfigDict(from_attributes=True)

    id: str

    @field_validator("id", mode="before")
    @classmethod
    def stringify_id(cls, value) -> str:
        return str(value)
