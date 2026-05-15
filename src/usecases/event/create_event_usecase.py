from __future__ import annotations

from src.models.event import EventCreate, EventEntity
from src.usecases.event.contracts import EventRepositoryProtocol

class CreateEventUseCase:
    def __init__(self, event_repository: EventRepositoryProtocol) -> None:
        self.event_repository = event_repository

    async def execute(self, event: EventCreate) -> EventEntity:
        return await self.event_repository.create(event)
