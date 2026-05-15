from __future__ import annotations

from datetime import date as date_type

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.contracts.event_repository import EventRepositoryProtocol
from src.contracts.subscription_repository import SubscriptionRepositoryProtocol
from src.models.subscription import Subscription, SubscriptionCreate


class CreateSubscriptionUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        subscription_repository: SubscriptionRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.subscription_repository = subscription_repository

    @staticmethod
    def _ensure_event_is_open_for_subscription(event) -> None:
        if event.date < date_type.today():
            raise HTTPException(
                status_code=409,
                detail="Cannot subscribe to an event that has already happened",
            )

    async def execute(
        self,
        data: SubscriptionCreate,
    ) -> Subscription:
        try:
            async with self.subscription_repository.transaction():
                event = await self.event_repository.get_by_id(data.event_id)
                if event is None:
                    raise HTTPException(status_code=404, detail="Event not found")
                self._ensure_event_is_open_for_subscription(event)

                if await self.subscription_repository.exists_by_email_and_event_id(
                    data.email,
                    data.event_id,
                ):
                    raise HTTPException(
                        status_code=409,
                        detail="This email is already subscribed to this event",
                    )

                return await self.subscription_repository.create(data)
        except IntegrityError as exc:
            raise HTTPException(
                status_code=409,
                detail="This email is already subscribed to this event",
            ) from exc
