from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any
from typing import Protocol

from fastapi_pagination import Params

from datetime import date as date_type

from src.models.subscription import (
    EventAttendanceRateRead,
    Subscription,
    SubscriptionCreate,
    SubscriptionUpdate,
)


class SubscriptionRepositoryProtocol(Protocol):
    def transaction(self) -> AsyncIterator[None]: ...

    async def create(self, data: SubscriptionCreate, event_id: str) -> Subscription: ...

    async def get_by_id(self, subscription_id: str) -> Subscription | None: ...

    async def list_paginated(
        self,
        params: Params,
        event_id: str | None = None,
        *,
        name: str | None = None,
        case_sensitive: bool = False,
        registered_from: date_type | None = None,
        registered_to: date_type | None = None,
    ) -> Any: ...

    async def exists_by_email_and_event_id(
        self,
        email: str,
        event_id: str,
        *,
        exclude_subscription_id: str | None = None,
    ) -> bool: ...

    async def count_with_check_in_aggregated(self, event_id: str) -> int: ...

    async def get_attendance_rate(self, event_id: str) -> EventAttendanceRateRead: ...

    async def update(
        self,
        subscription: Subscription,
        data: SubscriptionUpdate,
    ) -> Subscription: ...

    async def delete(self, subscription: Subscription) -> None: ...
