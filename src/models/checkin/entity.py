from datetime import datetime

from pydantic import BaseModel, Field


class CheckIn(BaseModel):
    timestamp: datetime
    access_point: str = Field(max_length=255)
