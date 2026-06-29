from __future__ import annotations

from fastapi import HTTPException, status
from fastapi.responses import Response

from src.contracts.document_repository import DocumentRepositoryProtocol
from src.core.uploads import build_document_object_name
from src.infra.storage import MinioStorageService


class DownloadDocumentUseCase:
    def __init__(
        self,
        document_repository: DocumentRepositoryProtocol,
        storage_service: MinioStorageService,
    ) -> None:
        self.document_repository = document_repository
        self.storage_service = storage_service

    async def execute(self, document_id: str) -> Response:
        document = await self.document_repository.get_by_id(document_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document not found")

        object_name = build_document_object_name(str(document.id), document.extension)
        try:
            content = await self.storage_service.download_file(object_name)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Physical document file not found",
            ) from exc

        return Response(
            content=content,
            media_type=document.content_type,
            headers={
                "Content-Disposition": f'attachment; filename="{document.original_filename}"',
            },
        )
