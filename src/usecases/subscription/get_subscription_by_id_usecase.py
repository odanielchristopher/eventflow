from __future__ import annotations

from fastapi import HTTPException

from src.contracts.event_repository import EventRepositoryProtocol
from src.contracts.subscription_repository import SubscriptionRepositoryProtocol
from src.models.subscription import Subscription


class GetSubscriptionByIdUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        subscription_repository: SubscriptionRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.subscription_repository = subscription_repository

    async def execute(self, event_id: int, subscription_id: int) -> Subscription:
        event = await self.event_repository.get_by_id(event_id)
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")

        subscription = await self.subscription_repository.get_by_id(subscription_id)
        if subscription is None or subscription.event_id != event_id:
            raise HTTPException(status_code=404, detail="Subscription not found")

        return subscription
