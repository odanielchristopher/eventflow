from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.speaker import Speaker, SpeakerCreate, SpeakerUpdate


class SqlModelSpeakerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        async with self.session.begin():
            yield

    async def create(self, data: SpeakerCreate) -> Speaker:
        speaker = Speaker.model_validate(data.model_dump())
        self.session.add(speaker)
        await self.session.flush()
        await self.session.refresh(speaker)
        return speaker

    async def get_by_id(self, speaker_id: int) -> Speaker | None:
        result = await self.session.execute(
            select(Speaker)
            .options(selectinload(Speaker.activities))
            .where(Speaker.id == speaker_id)
        )
        return result.scalar_one_or_none()

    async def list_paginated(self, params: Params) -> Any:
        query = select(Speaker).order_by(Speaker.name, Speaker.id)
        return await apaginate(self.session, query, params=params)

    async def update(self, speaker: Speaker, data: SpeakerUpdate) -> Speaker:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(speaker, field, value)

        self.session.add(speaker)
        await self.session.flush()
        await self.session.refresh(speaker)
        return speaker

    async def delete(self, speaker: Speaker) -> None:
        await self.session.delete(speaker)
