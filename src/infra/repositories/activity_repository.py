from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.activity import Activity, ActivityCreate, ActivityUpdate
from src.models.speaker import Speaker


class SqlModelActivityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        async with self.session.begin():
            yield

    def _base_query(self):
        return select(Activity).options(
            selectinload(Activity.event),
            selectinload(Activity.speakers),
        )

    async def _get_loaded_by_id(self, activity_id: int) -> Activity:
        result = await self.session.execute(
            self._base_query().where(Activity.id == activity_id)
        )
        return result.scalar_one()

    async def create(
        self,
        data: ActivityCreate,
        speakers: list[Speaker],
    ) -> Activity:
        activity = Activity.model_validate(data.model_dump(exclude={"speaker_ids"}))
        activity.speakers = speakers
        self.session.add(activity)
        await self.session.flush()
        if activity.id is None:
            raise RuntimeError("Activity ID was not generated")
        return await self._get_loaded_by_id(activity.id)

    async def get_by_id(self, activity_id: int) -> Activity | None:
        result = await self.session.execute(
            self._base_query().where(Activity.id == activity_id)
        )
        return result.scalar_one_or_none()

    async def list_paginated(self, params: Params, event_id: int | None = None) -> Any:
        query = self._base_query().order_by(Activity.scheduled_at, Activity.id)
        if event_id is not None:
            query = query.where(Activity.event_id == event_id)

        return await apaginate(self.session, query, params=params)

    async def update(
        self,
        activity: Activity,
        data: ActivityUpdate,
        speakers: list[Speaker] | None = None,
    ) -> Activity:
        for field, value in data.model_dump(
            exclude={"speaker_ids"},
            exclude_unset=True,
        ).items():
            setattr(activity, field, value)

        if speakers is not None:
            activity.speakers = speakers

        self.session.add(activity)
        await self.session.flush()
        if activity.id is None:
            raise RuntimeError("Activity ID was not generated")
        return await self._get_loaded_by_id(activity.id)

    async def delete(self, activity: Activity) -> None:
        await self.session.delete(activity)
