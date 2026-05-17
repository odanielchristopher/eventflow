from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any, Protocol

from fastapi_pagination import Params

from src.models.activity import Activity, ActivityCreate, ActivityUpdate
from src.models.speaker import Speaker


class ActivityRepositoryProtocol(Protocol):
    def transaction(self) -> AsyncIterator[None]: ...

    async def create(
        self,
        data: ActivityCreate,
        speakers: list[Speaker],
    ) -> Activity: ...

    async def get_by_id(self, activity_id: int) -> Activity | None: ...

    async def list_paginated(self, params: Params, event_id: int | None = None) -> Any: ...

    async def update(
        self,
        activity: Activity,
        data: ActivityUpdate,
        speakers: list[Speaker] | None = None,
    ) -> Activity: ...

    async def delete(self, activity: Activity) -> None: ...
