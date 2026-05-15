from __future__ import annotations

from typing import Any, Protocol

from fastapi_pagination import Params

from src.models.event import EventCreate, EventEntity, EventUpdate


class EventRepositoryProtocol(Protocol):
    async def list_paginated(self, params: Params) -> Any: ...

    async def get_by_id(self, event_id: int) -> EventEntity | None: ...

    async def create(self, data: EventCreate) -> EventEntity: ...

    async def update(self, event: EventEntity, data: EventUpdate) -> EventEntity: ...

    async def delete(self, event: EventEntity) -> None: ...
