from __future__ import annotations

from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError

from src.contracts.document_repository import DocumentRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol
from src.models.event import EventEntity, EventRead, EventUpdate
from src.usecases.event.presentation import serialize_event


class UpdateEventUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        document_repository: DocumentRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.document_repository = document_repository

    async def execute(
        self,
        event_id: str,
        update_dto: EventUpdate,
    ) -> EventRead:
        try:
            async with self.event_repository.transaction():
                event = await self.event_repository.get_by_id(event_id)

                if event is None:
                    raise HTTPException(status_code=404, detail="Event not found")

                await self._validate_update_rules(event, update_dto)
                updated_event = await self.event_repository.update(event, update_dto)
                documents = await self.document_repository.list_by_event_ids([event_id])
                return serialize_event(updated_event, documents)
        except DuplicateKeyError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Event violates a uniqueness constraint",
            ) from exc

    async def _validate_update_rules(self, event: EventEntity, update_dto: EventUpdate) -> None:
        next_title = update_dto.title if update_dto.title is not None else event.title
        next_description = (
            update_dto.description if update_dto.description is not None else event.description
        )
        next_date = update_dto.date if update_dto.date is not None else event.date
        next_location = update_dto.location if update_dto.location is not None else event.location

        if await self.event_repository.exists_by_title(next_title, exclude_event_id=str(event.id)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Event title already exists",
            )

        if await self.event_repository.exists_by_description(
            next_description,
            exclude_event_id=str(event.id),
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Event description already exists",
            )

        if await self.event_repository.exists_by_date_and_location(
            next_date,
            next_location,
            exclude_event_id=str(event.id),
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="There is already an event for this date and location",
            )
