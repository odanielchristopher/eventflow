from __future__ import annotations

from src.models.base import BaseModel
from src.models.event.event import Event


class ListEventsMeta(BaseModel):
    total: int
    page: int
    per_page: int


class ListEventsResponse(BaseModel):
    data: list[Event]
    meta: ListEventsMeta
