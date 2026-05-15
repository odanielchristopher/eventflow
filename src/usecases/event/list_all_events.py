from __future__ import annotations

from typing import Any

from fastapi_pagination import Params

from src.contracts.event_repository import EventRepositoryProtocol

class ListAllEventsUseCase:
    def __init__(self, event_repository: EventRepositoryProtocol) -> None:
        self.event_repository = event_repository

    async def execute(self, params: Params) -> Any:
        return await self.event_repository.list_paginated(params)
