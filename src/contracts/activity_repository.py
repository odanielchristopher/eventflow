from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import time as time_type
from typing import Any, Protocol

from fastapi_pagination import Params

from src.models.activity import Activity, ActivityCreate, ActivityUpdate


class ActivityRepositoryProtocol(Protocol):
    def transaction(self) -> AsyncIterator[None]: ...

    async def create(
        self,
        data: ActivityCreate,
        event_id: str,
    ) -> Activity: ...

    async def get_by_id(self, activity_id: str) -> Activity | None: ...

    async def list_paginated(
        self,
        params: Params,
        event_id: str | None = None,
        *,
        title: str | None = None,
        speaker_id: str | None = None,
        scheduled_from: time_type | None = None,
        scheduled_to: time_type | None = None,
        case_sensitive: bool = False,
    ) -> Any: ...

    async def update(
        self,
        activity: Activity,
        data: ActivityUpdate,
    ) -> Activity: ...

    async def delete(self, activity: Activity) -> None: ...
