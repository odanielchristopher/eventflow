from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.contracts.checkin_repository import CheckInRepositoryProtocol
from src.contracts.subscription_repository import SubscriptionRepositoryProtocol
from src.models.checkin import CheckIn, CheckInCreate
from src.models.subscription import Subscription


class CreateCheckInUseCase:
    def __init__(
        self,
        subscription_repository: SubscriptionRepositoryProtocol,
        check_in_repository: CheckInRepositoryProtocol,
    ) -> None:
        self.subscription_repository = subscription_repository
        self.check_in_repository = check_in_repository

    @staticmethod
    def _ensure_timestamp_matches_event_date(data: CheckInCreate, subscription: Subscription) -> None:
        if data.timestamp.date() != subscription.event.date:
            raise HTTPException(
                status_code=409,
                detail="Check-in timestamp must match the event date",
            )

    async def execute(self, data: CheckInCreate) -> CheckIn:
        try:
            async with self.check_in_repository.transaction():
                subscription = await self.subscription_repository.get_by_id(data.subscription_id)
                if subscription is None:
                    raise HTTPException(status_code=404, detail="Subscription not found")

                self._ensure_timestamp_matches_event_date(data, subscription)

                if await self.check_in_repository.exists_by_subscription_id(
                    data.subscription_id,
                ):
                    raise HTTPException(
                        status_code=409,
                        detail="Subscription already has a check-in",
                    )

                return await self.check_in_repository.create(data)
        except IntegrityError as exc:
            raise HTTPException(
                status_code=409,
                detail="Subscription already has a check-in",
            ) from exc
