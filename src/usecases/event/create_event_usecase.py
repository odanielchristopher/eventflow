from __future__ import annotations

from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError

from src.contracts.event_repository import EventRepositoryProtocol
from src.models.event import EventCreate, EventEntity


class CreateEventUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository

    async def execute(
        self,
        event: EventCreate,
    ) -> EventEntity:
        try:
            async with self.event_repository.transaction():
                await self._validate_create_rules(event)
                return await self.event_repository.create(event)
        except DuplicateKeyError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Event violates a uniqueness constraint",
            ) from exc

    async def _validate_create_rules(self, event: EventCreate) -> None:
        if await self.event_repository.exists_by_title(event.title):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Event title already exists",
            )

        if await self.event_repository.exists_by_description(event.description):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Event description already exists",
            )

        if await self.event_repository.exists_by_date_and_location(event.date, event.location):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="There is already an event for this date and location",
            )
