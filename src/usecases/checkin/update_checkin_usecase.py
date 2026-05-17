from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.contracts.checkin_repository import CheckInRepositoryProtocol
from src.contracts.subscription_repository import SubscriptionRepositoryProtocol
from src.models.checkin import CheckIn, CheckInUpdate
from src.models.subscription import Subscription


class UpdateCheckInUseCase:
    def __init__(
        self,
        subscription_repository: SubscriptionRepositoryProtocol,
        check_in_repository: CheckInRepositoryProtocol,
    ) -> None:
        self.subscription_repository = subscription_repository
        self.check_in_repository = check_in_repository

    @staticmethod
    def _ensure_timestamp_matches_event_date(timestamp, subscription: Subscription) -> None:
        if timestamp.date() != subscription.event.date:
            raise HTTPException(
                status_code=409,
                detail="Check-in timestamp must match the event date",
            )

    async def execute(self, check_in_id: int, data: CheckInUpdate) -> CheckIn:
        try:
            async with self.check_in_repository.transaction():
                check_in = await self.check_in_repository.get_by_id(check_in_id)
                if check_in is None:
                    raise HTTPException(status_code=404, detail="Check-in not found")

                next_subscription_id = (
                    data.subscription_id
                    if data.subscription_id is not None
                    else check_in.subscription_id
                )
                subscription = await self.subscription_repository.get_by_id(next_subscription_id)
                if subscription is None:
                    raise HTTPException(status_code=404, detail="Subscription not found")

                next_timestamp = data.timestamp if data.timestamp is not None else check_in.timestamp
                self._ensure_timestamp_matches_event_date(next_timestamp, subscription)

                if await self.check_in_repository.exists_by_subscription_id(
                    next_subscription_id,
                    exclude_check_in_id=check_in.id,
                ):
                    raise HTTPException(
                        status_code=409,
                        detail="Subscription already has a check-in",
                    )

                return await self.check_in_repository.update(check_in, data)
        except IntegrityError as exc:
            raise HTTPException(
                status_code=409,
                detail="Subscription already has a check-in",
            ) from exc
