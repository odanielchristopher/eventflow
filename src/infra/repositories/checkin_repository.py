from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.checkin import CheckIn, CheckInCreate, CheckInUpdate
from src.models.subscription import Subscription


class SqlModelCheckInRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        async with self.session.begin():
            yield

    def _base_query(self):
        return select(CheckIn).options(
            selectinload(CheckIn.subscription).selectinload(Subscription.event),
        )

    async def _get_loaded_by_id(self, check_in_id: int) -> CheckIn:
        result = await self.session.execute(
            self._base_query().where(CheckIn.id == check_in_id)
        )
        return result.scalar_one()

    async def create(self, data: CheckInCreate) -> CheckIn:
        check_in = CheckIn.model_validate(data.model_dump())
        self.session.add(check_in)
        await self.session.flush()
        if check_in.id is None:
            raise RuntimeError("Check-in ID was not generated")
        return await self._get_loaded_by_id(check_in.id)

    async def get_by_id(self, check_in_id: int) -> CheckIn | None:
        result = await self.session.execute(
            self._base_query().where(CheckIn.id == check_in_id)
        )
        return result.scalar_one_or_none()

    async def list_paginated(
        self,
        params: Params,
        event_id: int | None = None,
    ) -> Any:
        query = self._base_query().order_by(CheckIn.timestamp.desc(), CheckIn.id.desc())
        if event_id is not None:
            query = query.join(Subscription).where(Subscription.event_id == event_id)

        return await apaginate(self.session, query, params=params)

    async def exists_by_subscription_id(
        self,
        subscription_id: int,
        *,
        exclude_check_in_id: int | None = None,
    ) -> bool:
        query = select(CheckIn.id).where(CheckIn.subscription_id == subscription_id)
        if exclude_check_in_id is not None:
            query = query.where(CheckIn.id != exclude_check_in_id)

        result = await self.session.execute(query.limit(1))
        return result.scalar_one_or_none() is not None

    async def update(self, check_in: CheckIn, data: CheckInUpdate) -> CheckIn:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(check_in, field, value)

        self.session.add(check_in)
        await self.session.flush()
        if check_in.id is None:
            raise RuntimeError("Check-in ID was not generated")
        return await self._get_loaded_by_id(check_in.id)

    async def delete(self, check_in: CheckIn) -> None:
        await self.session.delete(check_in)
