from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any
from typing import Protocol

from fastapi_pagination import Params

from src.models.subscription import Subscription, SubscriptionCreate, SubscriptionUpdate


class SubscriptionRepositoryProtocol(Protocol):
    def transaction(self) -> AsyncIterator[None]: ...

    async def create(self, data: SubscriptionCreate) -> Subscription: ...

    async def get_by_id(self, subscription_id: int) -> Subscription | None: ...

    async def list_paginated(self, params: Params, event_id: int | None = None) -> Any: ...

    async def exists_by_email_and_event_id(
        self,
        email: str,
        event_id: int,
        *,
        exclude_subscription_id: int | None = None,
    ) -> bool: ...

    async def update(
        self,
        subscription: Subscription,
        data: SubscriptionUpdate,
    ) -> Subscription: ...

    async def delete(self, subscription: Subscription) -> None: ...
