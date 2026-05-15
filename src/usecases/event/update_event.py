from __future__ import annotations

import logging

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.exc import IntegrityError

from src.contracts.document_repository import DocumentRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol
from src.core.uploads import (
    build_document_filename,
    build_document_url,
    delete_upload_by_filename,
    ensure_image_upload,
    get_upload_extension,
    save_upload_file,
)
from src.models.document import DocumentCreate
from src.models.event import EventEntity, EventUpdate


logger = logging.getLogger(__name__)


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
        event_id: int,
        update_dto: EventUpdate,
        banner_image: UploadFile | None = None,
    ) -> EventEntity:
        saved_filename: str | None = None
        event: EventEntity | None = None
        try:
            async with self.event_repository.transaction():
                event = await self.event_repository.get_by_id(event_id)

                if event is None:
                    raise HTTPException(status_code=404, detail="Event not found")

                await self._validate_update_rules(event, update_dto)
                updated_event = await self.event_repository.update(event, update_dto)

                if banner_image is None:
                    return updated_event

                ensure_image_upload(banner_image)
                extension = get_upload_extension(banner_image)

                document = await self.document_repository.create(
                    DocumentCreate(
                        original_filename=banner_image.filename or f"banner.{extension}",
                        content_type=banner_image.content_type or "application/octet-stream",
                        extension=extension,
                        size_bytes=0,
                        event_id=updated_event.id,
                    )
                )

                saved_filename = build_document_filename(document.id, document.extension)
                size_bytes = await save_upload_file(banner_image, saved_filename)
                await self.document_repository.update_size_bytes(document, size_bytes)

                await self.event_repository.update(
                    updated_event,
                    EventUpdate(
                        banner_img_url=build_document_url(document.id, document.extension),
                    ),
                )

            return await self.event_repository.get_by_id(event_id) or event
        except IntegrityError as exc:
            delete_upload_by_filename(saved_filename)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Event violates a uniqueness constraint",
            ) from exc
        except HTTPException:
            delete_upload_by_filename(saved_filename)
            raise
        except Exception as exc:
            delete_upload_by_filename(saved_filename)
            logger.exception("Unexpected error while updating event with banner")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not update event with banner image",
            ) from exc

    async def _validate_update_rules(self, event: EventEntity, update_dto: EventUpdate) -> None:
        next_title = update_dto.title if update_dto.title is not None else event.title
        next_description = (
            update_dto.description if update_dto.description is not None else event.description
        )
        next_date = update_dto.date if update_dto.date is not None else event.date
        next_location = update_dto.location if update_dto.location is not None else event.location

        if await self.event_repository.exists_by_title(next_title, exclude_event_id=event.id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Event title already exists",
            )

        if await self.event_repository.exists_by_description(
            next_description,
            exclude_event_id=event.id,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Event description already exists",
            )

        if await self.event_repository.exists_by_date_and_location(
            next_date,
            next_location,
            exclude_event_id=event.id,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="There is already an event for this date and location",
            )
