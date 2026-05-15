from __future__ import annotations

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

    async def get_by_id(self, event_id: int) -> EventEntity | None:
        query = self._base_query().where(EventEntity.id == event_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, data: EventCreate) -> EventEntity:
        event = EventEntity.model_validate(data.model_dump())
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return await self.get_by_id(event.id) or event

    async def update(self, event: EventEntity, data: EventUpdate) -> EventEntity:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(event, field, value)

        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return await self.get_by_id(event.id) or event

    async def delete(self, event: EventEntity) -> None:
        await self.session.delete(event)
        await self.session.commit()
