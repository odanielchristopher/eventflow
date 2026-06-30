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
    DocumentUpdate,
)
from src.models.event import EventEntity, EventRead, EventUpdate
from src.usecases.event.presentation import serialize_event


class UpdateEventUseCase:
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
        event_id: str,
        update_dto: EventUpdate,
        banner_image: UploadFile | None = None,
        attachment_pdf: UploadFile | None = None,
    ) -> EventRead:
        try:
            async with self.event_repository.transaction():
                event = await self.event_repository.get_by_id(event_id)

                if event is None:
                    raise HTTPException(status_code=404, detail="Event not found")

                await self._validate_update_rules(event, update_dto)
                if banner_image is not None:
                    ensure_image_upload(banner_image)
                    banner_document = await self._upsert_document_for_role(
                        event_id,
                        banner_image,
                        BANNER_IMAGE_ROLE,
                    )
                    await self.event_repository.set_banner_url(
                        event,
                        build_document_download_url(str(banner_document.id)),
                    )

                if attachment_pdf is not None:
                    ensure_pdf_upload(attachment_pdf)
                    await self._upsert_document_for_role(
                        event_id,
                        attachment_pdf,
                        ATTACHMENT_PDF_ROLE,
                    )

                updated_event = await self.event_repository.update(event, update_dto)
                documents = await self.document_repository.list_by_event_ids([event_id])
                return serialize_event(updated_event, documents)
        except DuplicateKeyError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Event violates a uniqueness constraint",
            ) from exc
        except Exception as exc:
            if isinstance(exc, HTTPException):
                raise
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not update event",
            ) from exc

    async def _validate_update_rules(self, event: EventEntity, update_dto: EventUpdate) -> None:
        next_title = update_dto.title if update_dto.title is not None else event.title
        next_description = (
            update_dto.description if update_dto.description is not None else event.description
        )
        next_date = update_dto.date if update_dto.date is not None else event.date
        next_location = update_dto.location if update_dto.location is not None else event.location

        if await self.event_repository.exists_by_title(next_title, exclude_event_id=str(event.id)):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Event title already exists",
            )

        if await self.event_repository.exists_by_description(
            next_description,
            exclude_event_id=str(event.id),
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Event description already exists",
            )

        if await self.event_repository.exists_by_date_and_location(
            next_date,
            next_location,
            exclude_event_id=str(event.id),
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="There is already an event for this date and location",
            )

    async def _upsert_document_for_role(
        self,
        event_id: str,
        upload: UploadFile,
        role: str,
    ) -> Document:
        existing_document = await self.document_repository.get_by_event_id_and_role(event_id, role)
        if existing_document is None:
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
                return document
            except Exception:
                if document is not None:
                    await self.document_repository.delete(document)
                raise

        previous_object_name = build_document_object_name(
            str(existing_document.id),
            existing_document.extension,
        )
        extension = get_upload_extension(upload)
        object_name = build_document_object_name(str(existing_document.id), extension)
        try:
            size_bytes = await self.storage_service.upload_file(upload, object_name)
            document = await self.document_repository.update(
                existing_document,
                DocumentUpdate(
                    original_filename=upload.filename or f"{role}.{extension}",
                    content_type=upload.content_type or "application/octet-stream",
                    extension=extension,
                    size_bytes=size_bytes,
                    role=role,
                ),
            )
            if previous_object_name != object_name:
                await self.storage_service.delete_file(previous_object_name)
            return document
        except Exception:
            if previous_object_name != object_name:
                await self.storage_service.delete_file(object_name)
            raise
