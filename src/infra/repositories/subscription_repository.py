from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import apaginate
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

    async def list_paginated(self, params: Params, event_id: int | None = None) -> Any:
        query = select(Subscription).order_by(
            Subscription.registered_at.desc(),
            Subscription.id.desc(),
        )
        if event_id is not None:
            query = query.where(Subscription.event_id == event_id)

        return await apaginate(self.session, query, params=params)

    async def exists_by_email_and_event_id(
        self,
        email: str,
        event_id: int,
        *,
        exclude_subscription_id: int | None = None,
    ) -> bool:
        query = select(Subscription.id).where(
            Subscription.email == email,
            Subscription.event_id == event_id,
        )
        if exclude_subscription_id is not None:
            query = query.where(Subscription.id != exclude_subscription_id)

        result = await self.session.execute(query.limit(1))
        return result.scalar_one_or_none() is not None

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
