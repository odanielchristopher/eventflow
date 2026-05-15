from __future__ import annotations

import logging

from fastapi import HTTPException, UploadFile, status

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
from src.models.document import Document, DocumentCreate
from src.models.event import EventEntity


logger = logging.getLogger(__name__)


class CreateDocumentUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        document_repository: DocumentRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.document_repository = document_repository

    async def execute(self, event_id: int, upload: UploadFile) -> Document:
        ensure_image_upload(upload)

        saved_filename: str | None = None
        try:
            async with self.document_repository.transaction():
                event = await self.event_repository.get_by_id(event_id)
                if event is None:
                    raise HTTPException(status_code=404, detail="Event not found")

                extension = get_upload_extension(upload)
                document = await self.document_repository.create(
                    DocumentCreate(
                        original_filename=upload.filename or f"banner.{extension}",
                        content_type=upload.content_type or "application/octet-stream",
                        extension=extension,
                        size_bytes=0,
                        event_id=event_id,
                    )
                )

                saved_filename = build_document_filename(document.id, document.extension)
                size_bytes = await save_upload_file(upload, saved_filename)
                document = await self.document_repository.update_size_bytes(document, size_bytes)
                await self.event_repository.set_banner_url(
                    event,
                    build_document_url(document.id, document.extension),
                )
                return document
        except HTTPException:
            delete_upload_by_filename(saved_filename)
            raise
        except Exception as exc:
            delete_upload_by_filename(saved_filename)
            logger.exception("Unexpected error while creating document for event")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create document for event",
            ) from exc
