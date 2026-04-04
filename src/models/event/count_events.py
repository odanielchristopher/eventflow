from __future__ import annotations

from src.models.base import BaseModel


class CountEventsResponse(BaseModel):
    total: int
