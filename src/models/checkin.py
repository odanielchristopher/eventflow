from __future__ import annotations

from datetime import datetime

from src.models.domain import DomainModel


class CheckIn(DomainModel):
    registration_id: int
    timestamp: datetime
    access_point: str
