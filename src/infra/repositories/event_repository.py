from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import date as date_type
from decimal import Decimal
import re
from typing import Any

from beanie import PydanticObjectId
from fastapi import HTTPException
from fastapi_pagination import Params, create_page

from src.models.event import EventCreate, EventEntity, EventUpdate


class BeanieEventRepository:
    def __init__(self, session: object | None = None) -> None:
        self.session = session

    async def list_paginated(self, params: Params) -> Any:
        query = EventEntity.find_all().sort("date")
        total = await query.count()
        items = await query.skip((params.page - 1) * params.size).limit(params.size).to_list()
        return create_page(items, total=total, params=params)

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        yield

    async def get_by_id(self, event_id: str) -> EventEntity | None:
        try:
            return await EventEntity.get(PydanticObjectId(event_id))
        except Exception as exc:
            raise HTTPException(status_code=422, detail="Invalid event id") from exc

    async def exists_by_title(
        self,
        title: str,
        *,
        exclude_event_id: str | None = None,
    ) -> bool:
        filters: dict[str, Any] = {"title": title}
        if exclude_event_id is not None:
            filters["_id"] = {"$ne": PydanticObjectId(exclude_event_id)}
        return await EventEntity.find_one(filters) is not None

    async def exists_by_description(
        self,
        description: str,
        *,
        exclude_event_id: str | None = None,
    ) -> bool:
        filters: dict[str, Any] = {"description": description}
        if exclude_event_id is not None:
            filters["_id"] = {"$ne": PydanticObjectId(exclude_event_id)}
        return await EventEntity.find_one(filters) is not None

    async def exists_by_date_and_location(
        self,
        event_date,
        location: str,
        *,
        exclude_event_id: str | None = None,
    ) -> bool:
        filters: dict[str, Any] = {"date": event_date, "location": location}
        if exclude_event_id is not None:
            filters["_id"] = {"$ne": PydanticObjectId(exclude_event_id)}
        return await EventEntity.find_one(filters) is not None

    async def create(self, data: EventCreate) -> EventEntity:
        event = EventEntity(**data.model_dump())
        await event.insert()
        return event

    async def update(self, event: EventEntity, data: EventUpdate) -> EventEntity:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(event, field, value)

        await event.save()
        return event

    async def delete(self, event: EventEntity) -> None:
        await event.delete()

    async def set_banner_url(self, event: EventEntity, banner_img_url: str | None) -> EventEntity:
        event.banner_img_url = banner_img_url
        await event.save()
        return event

    async def count_filtered(
        self,
        *,
        date_from: date_type | None = None,
        date_to: date_type | None = None,
        location: str | None = None,
        title: str | None = None,
        case_sensitive: bool = False,
    ) -> int:
        filters = self._build_analytics_filters(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            case_sensitive=case_sensitive,
        )
        pipeline = [{"$match": filters}, {"$count": "count"}]
        result = await EventEntity.aggregate(pipeline).to_list()
        return int(result[0]["count"]) if result else 0

    async def list_by_subscription_price_range(
        self,
        params: Params,
        *,
        min_price: Decimal,
        max_price: Decimal,
        date_from: date_type | None = None,
        date_to: date_type | None = None,
        location: str | None = None,
        title: str | None = None,
        case_sensitive: bool = False,
    ) -> Any:
        filters = self._build_analytics_filters(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            case_sensitive=case_sensitive,
        )
        filters["sub_price"] = {"$gte": min_price, "$lte": max_price}
        query = EventEntity.find(filters).sort("sub_price", "_id")
        total = await query.count()
        items = await query.skip((params.page - 1) * params.size).limit(params.size).to_list()
        return create_page(items, total=total, params=params)

    def _build_analytics_filters(
        self,
        *,
        date_from: date_type | None = None,
        date_to: date_type | None = None,
        location: str | None = None,
        title: str | None = None,
        case_sensitive: bool = False,
    ) -> dict[str, Any]:
        filters: dict[str, Any] = {}
        if date_from is not None or date_to is not None:
            date_filter: dict[str, date_type] = {}
            if date_from is not None:
                date_filter["$gte"] = date_from
            if date_to is not None:
                date_filter["$lte"] = date_to
            filters["date"] = date_filter

        regex_options = "" if case_sensitive else "i"
        if location:
            location_filter: dict[str, str] = {"$regex": re.escape(location)}
            if regex_options:
                location_filter["$options"] = regex_options
            filters["location"] = location_filter
        if title:
            title_filter: dict[str, str] = {"$regex": re.escape(title)}
            if regex_options:
                title_filter["$options"] = regex_options
            filters["title"] = title_filter
        return filters
