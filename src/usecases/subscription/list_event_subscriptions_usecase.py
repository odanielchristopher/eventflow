from __future__ import annotations

from typing import Any

from fastapi import HTTPException
from fastapi_pagination import Params

from src.contracts.event_repository import EventRepositoryProtocol
from src.contracts.subscription_repository import SubscriptionRepositoryProtocol


class ListEventSubscriptionsUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        subscription_repository: SubscriptionRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.subscription_repository = subscription_repository

    async def execute(self, params: Params, event_id: int | None = None) -> Any:
        if event_id is not None:
            event = await self.event_repository.get_by_id(event_id)
            if event is None:
                raise HTTPException(status_code=404, detail="Event not found")

        return await self.subscription_repository.list_paginated(params, event_id)
