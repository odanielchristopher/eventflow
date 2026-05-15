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
from src.models.document import Document, DocumentUpdate


logger = logging.getLogger(__name__)


class ReplaceDocumentUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        document_repository: DocumentRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.document_repository = document_repository

    async def execute(self, document_id: int, upload: UploadFile) -> Document:
        ensure_image_upload(upload)

        saved_filename: str | None = None
        previous_filename: str | None = None
        try:
            async with self.document_repository.transaction():
                document = await self.document_repository.get_by_id(document_id)
                if document is None:
                    raise HTTPException(status_code=404, detail="Document not found")

                previous_filename = build_document_filename(document.id, document.extension)
                extension = get_upload_extension(upload)

                document = await self.document_repository.update(
                    document,
                    DocumentUpdate(
                        original_filename=upload.filename or f"banner.{extension}",
                        content_type=upload.content_type or "application/octet-stream",
                        extension=extension,
                    ),
                )

                saved_filename = build_document_filename(document.id, document.extension)
                size_bytes = await save_upload_file(upload, saved_filename)
                document = await self.document_repository.update_size_bytes(document, size_bytes)

                if previous_filename and previous_filename != saved_filename:
                    delete_upload_by_filename(previous_filename)

                if document.event_id is not None and document.event is not None:
                    await self.event_repository.set_banner_url(
                        document.event,
                        build_document_url(document.id, document.extension),
                    )

                return document
        except HTTPException:
            if saved_filename and saved_filename != previous_filename:
                delete_upload_by_filename(saved_filename)
            raise
        except Exception as exc:
            if saved_filename and saved_filename != previous_filename:
                delete_upload_by_filename(saved_filename)
            logger.exception("Unexpected error while replacing document file")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not replace document file",
            ) from exc
