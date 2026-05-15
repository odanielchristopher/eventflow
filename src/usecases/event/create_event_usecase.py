from __future__ import annotations

import logging

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.exc import IntegrityError

from src.core.uploads import (
    build_document_filename,
    build_document_url,
    delete_upload_by_filename,
    ensure_image_upload,
    get_upload_extension,
    save_upload_file,
)
from src.models.document import DocumentCreate
from src.models.event import EventCreate, EventEntity, EventUpdate
from src.usecases.event.contracts import (
    DocumentRepositoryProtocol,
    EventRepositoryProtocol,
)


logger = logging.getLogger(__name__)


class CreateEventUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        document_repository: DocumentRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.document_repository = document_repository

    async def execute(
        self,
        event: EventCreate,
        banner_image: UploadFile | None = None,
    ) -> EventEntity:
        saved_filename: str | None = None
        created_event: EventEntity | None = None
        try:
            async with self.event_repository.transaction():
                await self._validate_create_rules(event)
                created_event = await self.event_repository.create(event)

                if banner_image is None:
                    return created_event

                ensure_image_upload(banner_image)
                extension = get_upload_extension(banner_image)

                document = await self.document_repository.create(
                    DocumentCreate(
                        original_filename=banner_image.filename or f"banner.{extension}",
                        content_type=banner_image.content_type or "application/octet-stream",
                        extension=extension,
                        size_bytes=0,
                        event_id=created_event.id,
                    )
                )

                saved_filename = build_document_filename(document.id, document.extension)
                size_bytes = await save_upload_file(banner_image, saved_filename)
                await self.document_repository.update_size_bytes(document, size_bytes)

                await self.event_repository.update(
                    created_event,
                    EventUpdate(
                        banner_img_url=build_document_url(document.id, document.extension)
                    ),
                )

            return await self.event_repository.get_by_id(created_event.id) or created_event
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
            logger.exception("Unexpected error while creating event with banner")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create event with banner image",
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
