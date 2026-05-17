from __future__ import annotations

from fastapi import HTTPException

from src.contracts.checkin_repository import CheckInRepositoryProtocol


class DeleteCheckInUseCase:
    def __init__(self, check_in_repository: CheckInRepositoryProtocol) -> None:
        self.check_in_repository = check_in_repository

    async def execute(self, check_in_id: int) -> None:
        async with self.check_in_repository.transaction():
            check_in = await self.check_in_repository.get_by_id(check_in_id)
            if check_in is None:
                raise HTTPException(status_code=404, detail="Check-in not found")

            await self.check_in_repository.delete(check_in)
