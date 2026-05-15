from __future__ import annotations

from pathlib import Path

from fastapi import HTTPException, status
from fastapi.responses import FileResponse

from src.contracts.document_repository import DocumentRepositoryProtocol
from src.core.config import get_settings
from src.core.uploads import build_document_filename


settings = get_settings()


class DownloadDocumentUseCase:
    def __init__(self, document_repository: DocumentRepositoryProtocol) -> None:
        self.document_repository = document_repository

    async def execute(self, document_id: int) -> FileResponse:
        document = await self.document_repository.get_by_id(document_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document not found")

        filename = build_document_filename(document.id, document.extension)
        path = settings.resolved_upload_dir / filename
        if not path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Physical document file not found",
            )

        return FileResponse(
            path=path,
            media_type=document.content_type,
            filename=document.original_filename,
        )
