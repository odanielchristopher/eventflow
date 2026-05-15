from __future__ import annotations

from fastapi import HTTPException

from src.contracts.document_repository import DocumentRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol
from src.models.document import Document


class ListEventDocumentsUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        document_repository: DocumentRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.document_repository = document_repository

    async def execute(self, event_id: int) -> list[Document]:
        event = await self.event_repository.get_by_id(event_id)
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")

        return await self.document_repository.list_by_event_id(event_id)
