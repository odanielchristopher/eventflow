from __future__ import annotations

from fastapi import HTTPException

from src.contracts.subscription_repository import SubscriptionRepositoryProtocol


class DeleteSubscriptionUseCase:
    def __init__(self, subscription_repository: SubscriptionRepositoryProtocol) -> None:
        self.subscription_repository = subscription_repository

    async def execute(self, subscription_id: int) -> None:
        async with self.subscription_repository.transaction():
            subscription = await self.subscription_repository.get_by_id(subscription_id)
            if subscription is None:
                raise HTTPException(status_code=404, detail="Subscription not found")

            await self.subscription_repository.delete(subscription)
