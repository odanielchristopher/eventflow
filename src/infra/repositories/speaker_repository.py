from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import re
from typing import Any

from beanie import PydanticObjectId
from fastapi import HTTPException
from fastapi_pagination import Params
from fastapi_pagination import create_page

from src.models.speaker import Speaker, SpeakerCreate, SpeakerUpdate


class BeanieSpeakerRepository:
    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        yield

    async def create(self, data: SpeakerCreate) -> Speaker:
        speaker = Speaker(**data.model_dump())
        await speaker.insert()
        return speaker

    async def get_by_id(self, speaker_id: str) -> Speaker | None:
        try:
            return await Speaker.get(PydanticObjectId(speaker_id))
        except Exception as exc:
            raise HTTPException(status_code=422, detail="Invalid speaker id") from exc

    async def list_by_ids(self, speaker_ids: list[str | int]) -> list[Speaker]:
        object_ids: list[PydanticObjectId] = []
        for speaker_id in speaker_ids:
            try:
                object_ids.append(PydanticObjectId(str(speaker_id)))
            except Exception:
                continue

        if not object_ids:
            return []

        return await Speaker.find({"_id": {"$in": object_ids}}).sort("name", "_id").to_list()

    async def list_paginated(
        self,
        params: Params,
        *,
        name: str | None = None,
        specialty: str | None = None,
        case_sensitive: bool = False,
    ) -> Any:
        filters: dict[str, Any] = {}
        if name:
            name_filter: dict[str, str] = {"$regex": re.escape(name)}
            if not case_sensitive:
                name_filter["$options"] = "i"
            filters["name"] = name_filter
        if specialty:
            specialty_filter: dict[str, str] = {"$regex": re.escape(specialty)}
            if not case_sensitive:
                specialty_filter["$options"] = "i"
            filters["specialty"] = specialty_filter

        query = Speaker.find(filters).sort("name", "_id")
        total = await query.count()
        items = await query.skip((params.page - 1) * params.size).limit(params.size).to_list()
        return create_page(items, total=total, params=params)

    async def update(self, speaker: Speaker, data: SpeakerUpdate) -> Speaker:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(speaker, field, value)

        await speaker.save()
        return speaker

    async def delete(self, speaker: Speaker) -> None:
        await speaker.delete()
