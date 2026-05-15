from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any, Protocol

from fastapi_pagination import Params

from src.models.event import EventCreate, EventEntity, EventUpdate


class EventRepositoryProtocol(Protocol):
    def transaction(self) -> AsyncIterator[None]: ...

    async def list_paginated(self, params: Params) -> Any: ...

    async def get_by_id(self, event_id: int) -> EventEntity | None: ...

    async def exists_by_title(
        self,
        title: str,
        *,
        exclude_event_id: int | None = None,
    ) -> bool: ...

    async def exists_by_description(
        self,
        description: str,
        *,
        exclude_event_id: int | None = None,
    ) -> bool: ...

    async def exists_by_date_and_location(
        self,
        event_date,
        location: str,
        *,
        exclude_event_id: int | None = None,
    ) -> bool: ...

    async def create(self, data: EventCreate) -> EventEntity: ...

    async def update(self, event: EventEntity, data: EventUpdate) -> EventEntity: ...

    async def delete(self, event: EventEntity) -> None: ...

    async def set_banner_url(
        self,
        event: EventEntity,
        banner_img_url: str | None,
    ) -> EventEntity: ...
