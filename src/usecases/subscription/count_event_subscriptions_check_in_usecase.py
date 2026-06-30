from __future__ import annotations

from fastapi import HTTPException

from src.contracts.event_repository import EventRepositoryProtocol
from src.contracts.subscription_repository import SubscriptionRepositoryProtocol
from src.models.subscription import SubscriptionCheckInCountRead


class CountEventSubscriptionsCheckInUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        subscription_repository: SubscriptionRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.subscription_repository = subscription_repository

    async def execute(self, event_id: str) -> SubscriptionCheckInCountRead:
        event = await self.event_repository.get_by_id(event_id)
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")

        count = await self.subscription_repository.count_with_check_in(event_id)
        return SubscriptionCheckInCountRead(count=count)
