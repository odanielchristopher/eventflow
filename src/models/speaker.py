from __future__ import annotations

from src.models.domain import DomainModel


class Speaker(DomainModel):
    name: str
    specialty: str
    bio: str
