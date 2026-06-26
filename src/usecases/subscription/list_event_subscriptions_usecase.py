from __future__ import annotations

from datetime import date as date_type
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

    async def execute(
        self,
        event_id: str,
        params: Params,
        *,
        name: str | None = None,
        case_sensitive: bool = False,
        registered_from: date_type | None = None,
        registered_to: date_type | None = None,
    ) -> Any:
        event = await self.event_repository.get_by_id(event_id)
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")

        return await self.subscription_repository.list_paginated(
            params,
            event_id,
            name=name,
            case_sensitive=case_sensitive,
            registered_from=registered_from,
            registered_to=registered_to,
        )
