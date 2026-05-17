from __future__ import annotations

from typing import Any

from fastapi import HTTPException
from fastapi_pagination import Params

from src.contracts.activity_repository import ActivityRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol


class ListActivitiesUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        activity_repository: ActivityRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.activity_repository = activity_repository

    async def execute(self, event_id: int, params: Params) -> Any:
        event = await self.event_repository.get_by_id(event_id)
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")

        return await self.activity_repository.list_paginated(params, event_id)
