from __future__ import annotations

from fastapi import HTTPException

from src.contracts.document_repository import DocumentRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol
from src.core.uploads import build_document_object_name
from src.infra.storage import MinioStorageService

class DeleteEventUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        document_repository: DocumentRepositoryProtocol,
        storage_service: MinioStorageService,
    ) -> None:
        self.event_repository = event_repository
        self.document_repository = document_repository
        self.storage_service = storage_service

    async def execute(self, event_id: str) -> None:
        event = await self.event_repository.get_by_id(event_id)

        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")

        documents = await self.document_repository.list_by_event_ids([event_id])
        for document in documents:
            await self.document_repository.delete(document)
            await self.storage_service.delete_file(
                build_document_object_name(str(document.id), document.extension),
            )

        await self.event_repository.delete(event)
