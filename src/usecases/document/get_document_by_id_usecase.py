from __future__ import annotations

from fastapi import HTTPException

from src.contracts.document_repository import DocumentRepositoryProtocol
from src.models.document import Document


class GetDocumentByIdUseCase:
    def __init__(self, document_repository: DocumentRepositoryProtocol) -> None:
        self.document_repository = document_repository

    async def execute(self, document_id: int) -> Document:
        document = await self.document_repository.get_by_id(document_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document not found")

        return document
