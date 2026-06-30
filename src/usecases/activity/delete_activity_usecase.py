from __future__ import annotations

from fastapi import HTTPException

from src.contracts.activity_repository import ActivityRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol


class DeleteActivityUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        activity_repository: ActivityRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.activity_repository = activity_repository

    async def execute(self, event_id: str, activity_id: str) -> None:
        async with self.activity_repository.transaction():
            event = await self.event_repository.get_by_id(event_id)
            if event is None:
                raise HTTPException(status_code=404, detail="Event not found")

            activity = await self.activity_repository.get_by_id(activity_id)
            if activity is None or activity.event_id != event_id:
                raise HTTPException(status_code=404, detail="Activity not found")

            await self.activity_repository.delete(activity)
