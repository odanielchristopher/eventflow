from __future__ import annotations

import logging

from fastapi import HTTPException, UploadFile, status

from src.contracts.document_repository import DocumentRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol
from src.core.uploads import (
    build_document_download_url,
    build_document_object_name,
    ensure_upload_matches_role,
    get_upload_extension,
    is_image_content_type,
)
from src.models.document import Document, DocumentUpdate
from src.models.document.roles import BANNER_IMAGE_ROLE
from src.infra.storage import MinioStorageService


logger = logging.getLogger(__name__)


class ReplaceDocumentUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        document_repository: DocumentRepositoryProtocol,
        storage_service: MinioStorageService,
    ) -> None:
        self.event_repository = event_repository
        self.document_repository = document_repository
        self.storage_service = storage_service

    async def execute(self, document_id: str, upload: UploadFile) -> Document:
        uploaded_object_name: str | None = None
        previous_object_name: str | None = None
        try:
            async with self.document_repository.transaction():
                document = await self.document_repository.get_by_id(document_id)
                if document is None:
                    raise HTTPException(status_code=404, detail="Document not found")

                ensure_upload_matches_role(upload, document.role)

                previous_object_name = build_document_object_name(str(document.id), document.extension)
                extension = get_upload_extension(upload)
                next_content_type = upload.content_type or "application/octet-stream"
                uploaded_object_name = build_document_object_name(str(document.id), extension)
                size_bytes = await self.storage_service.upload_file(upload, uploaded_object_name)

                document = await self.document_repository.update(
                    document,
                    DocumentUpdate(
                        original_filename=upload.filename or f"document.{extension}",
                        content_type=next_content_type,
                        extension=extension,
                        size_bytes=size_bytes,
                    ),
                )

                if document.event_id is not None:
                    event = await self.event_repository.get_by_id(document.event_id)
                    if event is not None:
                        current_document_url = build_document_download_url(str(document.id))
                        if document.role == BANNER_IMAGE_ROLE and is_image_content_type(document.content_type):
                            await self.event_repository.set_banner_url(event, current_document_url)
                        elif event.banner_img_url == current_document_url:
                            await self.event_repository.set_banner_url(event, None)

                if previous_object_name and previous_object_name != uploaded_object_name:
                    await self.storage_service.delete_file(previous_object_name)

                return document
        except HTTPException:
            if uploaded_object_name and uploaded_object_name != previous_object_name:
                await self.storage_service.delete_file(uploaded_object_name)
            raise
        except Exception as exc:
            if uploaded_object_name and uploaded_object_name != previous_object_name:
                await self.storage_service.delete_file(uploaded_object_name)
            logger.exception("Unexpected error while replacing document file")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not replace document file",
            ) from exc
