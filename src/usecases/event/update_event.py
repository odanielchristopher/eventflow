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
from src.models.event import EventEntity, EventUpdate
from src.usecases.event.contracts import (
    DocumentRepositoryProtocol,
    EventRepositoryProtocol,
)

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
        event = await self.event_repository.get_by_id(event_id)

        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")

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

        refreshed_event = await self.event_repository.update(
            updated_event,
            EventUpdate(
                banner_img_url=build_document_url(document.id, document.extension),
            ),
        )
        return refreshed_event
