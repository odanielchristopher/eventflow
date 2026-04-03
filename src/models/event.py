from __future__ import annotations

from datetime import date
from decimal import Decimal

from src.models.domain import DomainModel


class Event(DomainModel):
    title: str
    description: str
    date: date
    location: str
    capacity: int
    sub_price: Decimal
