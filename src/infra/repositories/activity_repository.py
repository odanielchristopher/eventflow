from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import time as time_type
import re
from typing import Any

from beanie import PydanticObjectId
from fastapi import HTTPException
from fastapi_pagination import Params, create_page

from src.models.activity import Activity, ActivityCreate, ActivityUpdate


class BeanieActivityRepository:
    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        yield

    async def create(
        self,
        data: ActivityCreate,
        event_id: str,
    ) -> Activity:
        activity = Activity(
            **data.model_dump(),
            event_id=event_id,
        )
        await activity.insert()
        return activity

    async def get_by_id(self, activity_id: str) -> Activity | None:
        try:
            return await Activity.get(PydanticObjectId(activity_id))
        except Exception as exc:
            raise HTTPException(status_code=422, detail="Invalid activity id") from exc

    async def list_paginated(
        self,
        params: Params,
        event_id: str | None = None,
        *,
        title: str | None = None,
        speaker_id: str | None = None,
        scheduled_from: time_type | None = None,
        scheduled_to: time_type | None = None,
        case_sensitive: bool = False,
    ) -> Any:
        filters: dict[str, Any] = {}
        if event_id is not None:
            filters["event_id"] = event_id
        if title:
            title_filter: dict[str, str] = {"$regex": re.escape(title)}
            if not case_sensitive:
                title_filter["$options"] = "i"
            filters["title"] = title_filter
        if speaker_id:
            filters["speaker_ids"] = speaker_id
        if scheduled_from is not None or scheduled_to is not None:
            time_filter: dict[str, str] = {}
            if scheduled_from is not None:
                time_filter["$gte"] = scheduled_from.isoformat()
            if scheduled_to is not None:
                time_filter["$lte"] = scheduled_to.isoformat()
            filters["scheduled_at"] = time_filter

        query = Activity.find(filters).sort("scheduled_at", "_id")
        total = await query.count()
        items = await query.skip((params.page - 1) * params.size).limit(params.size).to_list()
        return create_page(items, total=total, params=params)

    async def update(
        self,
        activity: Activity,
        data: ActivityUpdate,
    ) -> Activity:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(activity, field, value)

        await activity.save()
        return activity

    async def delete(self, activity: Activity) -> None:
        await activity.delete()
