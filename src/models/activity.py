from __future__ import annotations

from datetime import time

from src.models.domain import DomainModel


class Activity(DomainModel):
    title: str
    scheduled_at: time
    speaker_id: int
    event_id: int
