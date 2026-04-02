from __future__ import annotations

from datetime import date

from src.models.domain import DomainModel


class Registration(DomainModel):
    name: str
    email: str
    ticket_category: str
    price: float
    registered_at: date
