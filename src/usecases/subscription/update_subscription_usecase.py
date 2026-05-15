from __future__ import annotations

from fastapi import HTTPException

from src.contracts.event_repository import EventRepositoryProtocol
from src.contracts.subscription_repository import SubscriptionRepositoryProtocol
from src.models.subscription import Subscription, SubscriptionUpdate


class UpdateSubscriptionUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        subscription_repository: SubscriptionRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.subscription_repository = subscription_repository

    async def execute(
        self,
        subscription_id: int,
        data: SubscriptionUpdate,
    ) -> Subscription:
        async with self.subscription_repository.transaction():
            subscription = await self.subscription_repository.get_by_id(subscription_id)
            if subscription is None:
                raise HTTPException(status_code=404, detail="Subscription not found")

            next_event_id = (
                data.event_id if data.event_id is not None else subscription.event_id
            )
            event = await self.event_repository.get_by_id(next_event_id)
            if event is None:
                raise HTTPException(status_code=404, detail="Event not found")

            return await self.subscription_repository.update(subscription, data)
