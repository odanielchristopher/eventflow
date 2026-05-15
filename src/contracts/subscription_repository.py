from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Protocol

from src.models.subscription import Subscription, SubscriptionCreate, SubscriptionUpdate


class SubscriptionRepositoryProtocol(Protocol):
    def transaction(self) -> AsyncIterator[None]: ...

    async def create(self, data: SubscriptionCreate) -> Subscription: ...

    async def get_by_id(self, subscription_id: int) -> Subscription | None: ...

    async def list_by_event_id(self, event_id: int) -> list[Subscription]: ...

    async def update(
        self,
        subscription: Subscription,
        data: SubscriptionUpdate,
    ) -> Subscription: ...

    async def delete(self, subscription: Subscription) -> None: ...
