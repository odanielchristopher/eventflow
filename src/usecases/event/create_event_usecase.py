from __future__ import annotations

from fastapi import HTTPException, UploadFile, status
from pymongo.errors import DuplicateKeyError

from src.contracts.document_repository import DocumentRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol
from src.core.uploads import (
    build_document_download_url,
    build_document_object_name,
    ensure_image_upload,
    ensure_pdf_upload,
    get_upload_extension,
)
from src.infra.storage import MinioStorageService
from src.models.document import (
    ATTACHMENT_PDF_ROLE,
    BANNER_IMAGE_ROLE,
    Document,
    DocumentCreate,
)
from src.models.event import EventCreate, EventRead
from src.usecases.event.presentation import serialize_event


class CreateEventUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        document_repository: DocumentRepositoryProtocol,
        storage_service: MinioStorageService,
    ) -> None:
        self.event_repository = event_repository
        self.document_repository = document_repository
        self.storage_service = storage_service

    async def execute(
        self,
        event: EventCreate,
        banner_image: UploadFile,
        attachment_pdf: UploadFile,
    ) -> EventRead:
        created_event = None
        created_documents: list[Document] = []
        uploaded_object_names: list[str] = []
        try:
            async with self.event_repository.transaction():
                await self._validate_create_rules(event)
                ensure_image_upload(banner_image)
                ensure_pdf_upload(attachment_pdf)

                created_event = await self.event_repository.create(event)

                banner_document, banner_object_name = await self._create_document_for_event(
                    str(created_event.id),
                    banner_image,
                    BANNER_IMAGE_ROLE,
                )
                created_documents.append(banner_document)
                uploaded_object_names.append(banner_object_name)

                attachment_document, attachment_object_name = await self._create_document_for_event(
                    str(created_event.id),
                    attachment_pdf,
                    ATTACHMENT_PDF_ROLE,
                )
                created_documents.append(attachment_document)
                uploaded_object_names.append(attachment_object_name)

                await self.event_repository.set_banner_url(
                    created_event,
                    build_document_download_url(str(banner_document.id)),
                )
                return serialize_event(created_event, created_documents)
        except DuplicateKeyError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Event violates a uniqueness constraint",
            ) from exc
        except HTTPException:
            await self._cleanup(created_event, created_documents, uploaded_object_names)
            raise
        except Exception as exc:
            await self._cleanup(created_event, created_documents, uploaded_object_names)
            print(exc)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create event",
            ) from exc

    async def _validate_create_rules(self, event: EventCreate) -> None:
        if await self.event_repository.exists_by_title(event.title):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Event title already exists",
            )

        if await self.event_repository.exists_by_description(event.description):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Event description already exists",
            )

        if await self.event_repository.exists_by_date_and_location(event.date, event.location):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="There is already an event for this date and location",
            )

    async def _create_document_for_event(
        self,
        event_id: str,
        upload: UploadFile,
        role: str,
    ) -> tuple[Document, str]:
        document: Document | None = None
        extension = get_upload_extension(upload)
        try:
            document = await self.document_repository.create(
                DocumentCreate(
                    original_filename=upload.filename or f"{role}.{extension}",
                    content_type=upload.content_type or "application/octet-stream",
                    extension=extension,
                    size_bytes=0,
                    event_id=event_id,
                    role=role,
                )
            )
            object_name = build_document_object_name(str(document.id), document.extension)
            size_bytes = await self.storage_service.upload_file(upload, object_name)
            document = await self.document_repository.update_size_bytes(document, size_bytes)
            return document, object_name
        except Exception:
            if document is not None:
                await self.document_repository.delete(document)
            raise

    async def _cleanup(
        self,
        event,
        documents: list[Document],
        object_names: list[str],
    ) -> None:
        for object_name in reversed(object_names):
            await self.storage_service.delete_file(object_name)

        for document in reversed(documents):
            await self.document_repository.delete(document)

        if event is not None:
            await self.event_repository.delete(event)
