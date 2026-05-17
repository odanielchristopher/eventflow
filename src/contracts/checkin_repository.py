from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any, Protocol

from fastapi_pagination import Params

from src.models.checkin import CheckIn, CheckInCreate, CheckInUpdate


class CheckInRepositoryProtocol(Protocol):
    def transaction(self) -> AsyncIterator[None]: ...

    async def create(self, data: CheckInCreate) -> CheckIn: ...

    async def get_by_id(self, check_in_id: int) -> CheckIn | None: ...

    async def list_paginated(
        self,
        params: Params,
        event_id: int | None = None,
    ) -> Any: ...

    async def exists_by_subscription_id(
        self,
        subscription_id: int,
        *,
        exclude_check_in_id: int | None = None,
    ) -> bool: ...

    async def update(self, check_in: CheckIn, data: CheckInUpdate) -> CheckIn: ...

    async def delete(self, check_in: CheckIn) -> None: ...
