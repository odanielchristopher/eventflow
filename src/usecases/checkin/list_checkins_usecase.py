from __future__ import annotations

from typing import Any

from fastapi import HTTPException
from fastapi_pagination import Params

from src.contracts.checkin_repository import CheckInRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol


class ListCheckInsUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        check_in_repository: CheckInRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.check_in_repository = check_in_repository

    async def execute(self, params: Params, event_id: int | None = None) -> Any:
        if event_id is not None:
            event = await self.event_repository.get_by_id(event_id)
            if event is None:
                raise HTTPException(status_code=404, detail="Event not found")

        return await self.check_in_repository.list_paginated(params, event_id)
