from __future__ import annotations

from fastapi import HTTPException, UploadFile, status

from src.core.uploads import (
    build_document_filename,
    build_document_url,
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

        try:
            size_bytes = await save_upload_file(
                banner_image,
                build_document_filename(document.id, document.extension),
            )
            await self.document_repository.update_size_bytes(document, size_bytes)
        except Exception as exc:
            await self.document_repository.delete(document)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not save banner image",
            ) from exc

        await self.event_repository.update(
            created_event,
            EventUpdate(banner_img_url=build_document_url(document.id, document.extension)),
        )
        return await self.event_repository.get_by_id(created_event.id) or created_event
