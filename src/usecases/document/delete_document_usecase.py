from __future__ import annotations

import logging

from fastapi import HTTPException, status

from src.contracts.document_repository import DocumentRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol
from src.core.uploads import build_document_download_url, build_document_object_name
from src.infra.storage import MinioStorageService


logger = logging.getLogger(__name__)


class DeleteDocumentUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        document_repository: DocumentRepositoryProtocol,
        storage_service: MinioStorageService,
    ) -> None:
        self.event_repository = event_repository
        self.document_repository = document_repository
        self.storage_service = storage_service

    async def execute(self, document_id: str) -> None:
        try:
            async with self.document_repository.transaction():
                document = await self.document_repository.get_by_id(document_id)
                if document is None:
                    raise HTTPException(status_code=404, detail="Document not found")

                object_name = build_document_object_name(str(document.id), document.extension)
                event = None
                if document.event_id is not None:
                    event = await self.event_repository.get_by_id(document.event_id)
                await self.document_repository.delete(document)

                if event is not None and event.banner_img_url:
                    if event.banner_img_url == build_document_download_url(str(document.id)):
                        await self.event_repository.set_banner_url(event, None)

            await self.storage_service.delete_file(object_name)
        except HTTPException:
            raise
        except Exception as exc:
            logger.exception("Unexpected error while deleting document")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not delete document",
            ) from exc
