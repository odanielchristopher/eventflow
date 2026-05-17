from __future__ import annotations

from fastapi import HTTPException

from src.contracts.checkin_repository import CheckInRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol


class DeleteCheckInUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        check_in_repository: CheckInRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.check_in_repository = check_in_repository

    async def execute(self, event_id: int, check_in_id: int) -> None:
        async with self.check_in_repository.transaction():
            event = await self.event_repository.get_by_id(event_id)
            if event is None:
                raise HTTPException(status_code=404, detail="Event not found")

            check_in = await self.check_in_repository.get_by_id(check_in_id)
            if check_in is None or check_in.subscription.event_id != event_id:
                raise HTTPException(status_code=404, detail="Check-in not found")

            await self.check_in_repository.delete(check_in)
