from __future__ import annotations

import logging

from fastapi import HTTPException, status

from src.contracts.document_repository import DocumentRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol
from src.core.uploads import build_document_filename, delete_upload_by_filename


logger = logging.getLogger(__name__)


class DeleteDocumentUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        document_repository: DocumentRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.document_repository = document_repository

    async def execute(self, document_id: int) -> None:
        try:
            async with self.document_repository.transaction():
                document = await self.document_repository.get_by_id(document_id)
                if document is None:
                    raise HTTPException(status_code=404, detail="Document not found")

                filename = build_document_filename(document.id, document.extension)
                event = document.event
                await self.document_repository.delete(document)

                if event is not None and event.banner_img_url:
                    if event.banner_img_url.endswith(filename):
                        await self.event_repository.set_banner_url(event, None)

            delete_upload_by_filename(filename)
        except HTTPException:
            raise
        except Exception as exc:
            logger.exception("Unexpected error while deleting document")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not delete document",
            ) from exc
