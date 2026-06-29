from __future__ import annotations

import logging

from fastapi import HTTPException, UploadFile, status

from src.contracts.document_repository import DocumentRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol
from src.core.uploads import (
    build_document_download_url,
    build_document_object_name,
    ensure_document_upload,
    get_upload_extension,
    is_image_content_type,
)
from src.models.document import Document, DocumentCreate
from src.infra.storage import MinioStorageService


logger = logging.getLogger(__name__)


class CreateDocumentUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        document_repository: DocumentRepositoryProtocol,
        storage_service: MinioStorageService,
    ) -> None:
        self.event_repository = event_repository
        self.document_repository = document_repository
        self.storage_service = storage_service

    async def execute(self, event_id: str, upload: UploadFile) -> Document:
        ensure_document_upload(upload)

        document: Document | None = None
        object_name: str | None = None
        try:
            async with self.document_repository.transaction():
                event = await self.event_repository.get_by_id(event_id)
                if event is None:
                    raise HTTPException(status_code=404, detail="Event not found")

                extension = get_upload_extension(upload)
                document = await self.document_repository.create(
                    DocumentCreate(
                        original_filename=upload.filename or f"document.{extension}",
                        content_type=upload.content_type or "application/octet-stream",
                        extension=extension,
                        size_bytes=0,
                        event_id=event_id,
                    )
                )

                object_name = build_document_object_name(str(document.id), document.extension)
                size_bytes = await self.storage_service.upload_file(upload, object_name)
                document = await self.document_repository.update_size_bytes(document, size_bytes)

                if is_image_content_type(document.content_type):
                    await self.event_repository.set_banner_url(
                        event,
                        build_document_download_url(str(document.id)),
                    )
                return document
        except HTTPException:
            if object_name is not None:
                await self.storage_service.delete_file(object_name)
            if document is not None:
                await self.document_repository.delete(document)
            raise
        except Exception as exc:
            if object_name is not None:
                await self.storage_service.delete_file(object_name)
            if document is not None:
                await self.document_repository.delete(document)
            logger.exception("Unexpected error while creating document for event")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create document for event",
            ) from exc
