from __future__ import annotations

from fastapi import HTTPException

from src.contracts.subscription_repository import SubscriptionRepositoryProtocol
from src.models.subscription import Subscription


class GetSubscriptionByIdUseCase:
    def __init__(self, subscription_repository: SubscriptionRepositoryProtocol) -> None:
        self.subscription_repository = subscription_repository

    async def execute(self, subscription_id: int) -> Subscription:
        subscription = await self.subscription_repository.get_by_id(subscription_id)
        if subscription is None:
            raise HTTPException(status_code=404, detail="Subscription not found")

        return subscription
