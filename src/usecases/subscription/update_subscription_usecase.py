from __future__ import annotations

from datetime import date as date_type

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.contracts.event_repository import EventRepositoryProtocol
from src.contracts.subscription_repository import SubscriptionRepositoryProtocol
from src.models.subscription import Subscription, SubscriptionUpdate


class UpdateSubscriptionUseCase:
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
        subscription_id: int,
        data: SubscriptionUpdate,
    ) -> Subscription:
        try:
            async with self.subscription_repository.transaction():
                subscription = await self.subscription_repository.get_by_id(subscription_id)
                if subscription is None:
                    raise HTTPException(status_code=404, detail="Subscription not found")

                next_event_id = (
                    data.event_id if data.event_id is not None else subscription.event_id
                )
                event = await self.event_repository.get_by_id(next_event_id)
                if event is None:
                    raise HTTPException(status_code=404, detail="Event not found")
                self._ensure_event_is_open_for_subscription(event)

                next_email = data.email if data.email is not None else subscription.email
                if await self.subscription_repository.exists_by_email_and_event_id(
                    next_email,
                    next_event_id,
                    exclude_subscription_id=subscription.id,
                ):
                    raise HTTPException(
                        status_code=409,
                        detail="This email is already subscribed to this event",
                    )

                return await self.subscription_repository.update(subscription, data)
        except IntegrityError as exc:
            raise HTTPException(
                status_code=409,
                detail="This email is already subscribed to this event",
            ) from exc
