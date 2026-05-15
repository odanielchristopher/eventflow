from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.event import EventCreate, EventEntity, EventUpdate


class SqlModelEventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _base_query(self):
        return (
            select(EventEntity)
            .options(selectinload(EventEntity.documents))
            .order_by(EventEntity.id)
        )

    async def list_paginated(self, params: Params) -> Any:
        return await apaginate(self.session, self._base_query(), params=params)

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        async with self.session.begin():
            yield

    async def get_by_id(self, event_id: int) -> EventEntity | None:
        query = self._base_query().where(EventEntity.id == event_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def exists_by_title(
        self,
        title: str,
        *,
        exclude_event_id: int | None = None,
    ) -> bool:
        query = select(EventEntity.id).where(EventEntity.title == title)
        if exclude_event_id is not None:
            query = query.where(EventEntity.id != exclude_event_id)
        result = await self.session.execute(query.limit(1))
        return result.scalar_one_or_none() is not None

    async def exists_by_description(
        self,
        description: str,
        *,
        exclude_event_id: int | None = None,
    ) -> bool:
        query = select(EventEntity.id).where(EventEntity.description == description)
        if exclude_event_id is not None:
            query = query.where(EventEntity.id != exclude_event_id)
        result = await self.session.execute(query.limit(1))
        return result.scalar_one_or_none() is not None

    async def exists_by_date_and_location(
        self,
        event_date,
        location: str,
        *,
        exclude_event_id: int | None = None,
    ) -> bool:
        query = select(EventEntity.id).where(
            EventEntity.date == event_date,
            EventEntity.location == location,
        )
        if exclude_event_id is not None:
            query = query.where(EventEntity.id != exclude_event_id)
        result = await self.session.execute(query.limit(1))
        return result.scalar_one_or_none() is not None

    async def create(self, data: EventCreate) -> EventEntity:
        event = EventEntity.model_validate(data.model_dump())
        self.session.add(event)
        await self.session.flush()
        await self.session.refresh(event)
        return event

    async def update(self, event: EventEntity, data: EventUpdate) -> EventEntity:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(event, field, value)

        self.session.add(event)
        await self.session.flush()
        await self.session.refresh(event)
        return event

    async def delete(self, event: EventEntity) -> None:
        await self.session.delete(event)

    async def set_banner_url(self, event: EventEntity, banner_img_url: str | None) -> EventEntity:
        event.banner_img_url = banner_img_url
        self.session.add(event)
        await self.session.flush()
        await self.session.refresh(event)
        return event
