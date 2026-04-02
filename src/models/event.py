from __future__ import annotations

from datetime import date

from src.models.domain import DomainModel


class Event(DomainModel):
    title: str
    date: date
    location: str
    capacity: int
