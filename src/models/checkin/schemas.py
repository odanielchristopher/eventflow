from __future__ import annotations

from datetime import datetime

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class CheckInBase(SQLModel):
    timestamp: datetime
    access_point: str = Field(max_length=255)
    subscription_id: int


class CheckInCreate(CheckInBase):
    pass


class CheckInUpdate(SQLModel):
    timestamp: datetime | None = None
    access_point: str | None = Field(default=None, max_length=255)
    subscription_id: int | None = None


class CheckInRead(CheckInBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
