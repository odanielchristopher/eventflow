from __future__ import annotations

from fastapi import HTTPException

from src.contracts.event_repository import EventRepositoryProtocol

class DeleteEventUseCase:
    def __init__(self, event_repository: EventRepositoryProtocol) -> None:
        self.event_repository = event_repository

    async def execute(self, event_id: int) -> None:
        event = await self.event_repository.get_by_id(event_id)

        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")

        await self.event_repository.delete(event)
