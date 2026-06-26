from __future__ import annotations

from datetime import datetime

from pydantic import ConfigDict
from pydantic import BaseModel, Field


class CheckInBase(BaseModel):
    timestamp: datetime
    access_point: str = Field(max_length=255)


class CheckInCreate(CheckInBase):
    pass


class CheckInUpdate(BaseModel):
    timestamp: datetime | None = None
    access_point: str | None = Field(default=None, max_length=255)


class CheckInRead(CheckInBase):
    model_config = ConfigDict(from_attributes=True)
