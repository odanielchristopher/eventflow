from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.subscription import Subscription, SubscriptionCreate, SubscriptionUpdate


class SqlModelSubscriptionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        async with self.session.begin():
            yield

    async def create(self, data: SubscriptionCreate) -> Subscription:
        subscription = Subscription.model_validate(data.model_dump())
        self.session.add(subscription)
        await self.session.flush()
        await self.session.refresh(subscription)
        return subscription

    async def get_by_id(self, subscription_id: int) -> Subscription | None:
        result = await self.session.execute(
            select(Subscription)
            .options(selectinload(Subscription.event))
            .where(Subscription.id == subscription_id)
        )
        return result.scalar_one_or_none()

    async def list_by_event_id(self, event_id: int) -> list[Subscription]:
        result = await self.session.execute(
            select(Subscription)
            .where(Subscription.event_id == event_id)
            .order_by(Subscription.registered_at.desc(), Subscription.id.desc())
        )
        return list(result.scalars().all())

    async def update(
        self,
        subscription: Subscription,
        data: SubscriptionUpdate,
    ) -> Subscription:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(subscription, field, value)

        self.session.add(subscription)
        await self.session.flush()
        await self.session.refresh(subscription)
        return subscription

    async def delete(self, subscription: Subscription) -> None:
        await self.session.delete(subscription)
