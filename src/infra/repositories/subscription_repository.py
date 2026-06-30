from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import date as date_type
import re
from typing import Any

from beanie import PydanticObjectId
from fastapi import HTTPException
from fastapi_pagination import Params, create_page

from src.models.subscription import (
    EventAttendanceRateRead,
    Subscription,
    SubscriptionCreate,
    SubscriptionUpdate,
)


class SqlModelSubscriptionRepository:
    def __init__(self, session: object | None = None) -> None:
        self.session = session

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        yield

    async def create(self, data: SubscriptionCreate, event_id: str) -> Subscription:
        subscription = Subscription(**data.model_dump(), event_id=event_id)
        await subscription.insert()
        return subscription

    async def get_by_id(self, subscription_id: str) -> Subscription | None:
        try:
            return await Subscription.get(PydanticObjectId(subscription_id))
        except Exception as exc:
            raise HTTPException(status_code=422, detail="Invalid subscription id") from exc

    async def list_paginated(
        self,
        params: Params,
        event_id: str | None = None,
        *,
        name: str | None = None,
        case_sensitive: bool = False,
        registered_from: date_type | None = None,
        registered_to: date_type | None = None,
    ) -> Any:
        filters: dict[str, Any] = {}
        if event_id is not None:
            filters["event_id"] = event_id
        if name:
            name_filter: dict[str, str] = {"$regex": re.escape(name)}
            if not case_sensitive:
                name_filter["$options"] = "i"
            filters["name"] = name_filter
        if registered_from is not None or registered_to is not None:
            date_filter: dict[str, date_type] = {}
            if registered_from is not None:
                date_filter["$gte"] = registered_from
            if registered_to is not None:
                date_filter["$lte"] = registered_to
            filters["registered_at"] = date_filter

        query = Subscription.find(filters).sort("-registered_at", "-_id")
        total = await query.count()
        items = await query.skip((params.page - 1) * params.size).limit(params.size).to_list()
        return create_page(items, total=total, params=params)

    async def exists_by_email_and_event_id(
        self,
        email: str,
        event_id: str,
        *,
        exclude_subscription_id: str | None = None,
    ) -> bool:
        filters: dict[str, Any] = {"email": email, "event_id": event_id}
        if exclude_subscription_id is not None:
            filters["_id"] = {"$ne": PydanticObjectId(exclude_subscription_id)}

        return await Subscription.find_one(filters) is not None

    async def count_with_check_in_aggregated(self, event_id: str) -> int:
        pipeline = [
            {
                "$match": {
                    "event_id": event_id,
                    "check_in": {"$ne": None},
                }
            },
            {"$count": "count"},
        ]
        result = await Subscription.aggregate(pipeline).to_list()
        return int(result[0]["count"]) if result else 0

    async def get_attendance_rate(self, event_id: str) -> EventAttendanceRateRead:
        pipeline = [
            {"$match": {"event_id": event_id}},
            {
                "$group": {
                    "_id": "$event_id",
                    "subscriptions_count": {"$sum": 1},
                    "check_ins_count": {
                        "$sum": {
                            "$cond": [
                                {"$ne": ["$check_in", None]},
                                1,
                                0,
                            ]
                        }
                    },
                }
            },
        ]
        result = await Subscription.aggregate(pipeline).to_list()
        if not result:
            return EventAttendanceRateRead(
                event_id=event_id,
                subscriptions_count=0,
                check_ins_count=0,
                attendance_rate=0,
            )

        row = result[0]
        subscriptions_count = int(row["subscriptions_count"])
        check_ins_count = int(row["check_ins_count"])
        attendance_rate = (
            check_ins_count / subscriptions_count if subscriptions_count > 0 else 0
        )
        return EventAttendanceRateRead(
            event_id=event_id,
            subscriptions_count=subscriptions_count,
            check_ins_count=check_ins_count,
            attendance_rate=attendance_rate,
        )

    async def update(
        self,
        subscription: Subscription,
        data: SubscriptionUpdate,
    ) -> Subscription:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(subscription, field, value)

        await subscription.save()
        return subscription

    async def delete(self, subscription: Subscription) -> None:
        await subscription.delete()
