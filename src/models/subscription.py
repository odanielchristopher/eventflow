from __future__ import annotations

from datetime import date

from src.models.domain import DomainModel


class Subscription(DomainModel):
    name: str
    email: str
    price: float
    registered_at: date
    event_id: int
