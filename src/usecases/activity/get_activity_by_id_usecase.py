from __future__ import annotations

from fastapi import HTTPException

from src.contracts.activity_repository import ActivityRepositoryProtocol
from src.models.activity import Activity


class GetActivityByIdUseCase:
    def __init__(self, activity_repository: ActivityRepositoryProtocol) -> None:
        self.activity_repository = activity_repository

    async def execute(self, activity_id: int) -> Activity:
        activity = await self.activity_repository.get_by_id(activity_id)
        if activity is None:
            raise HTTPException(status_code=404, detail="Activity not found")

        return activity
