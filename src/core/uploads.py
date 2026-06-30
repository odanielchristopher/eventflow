from __future__ import annotations

import mimetypes
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from src.models.document.roles import ATTACHMENT_PDF_ROLE, BANNER_IMAGE_ROLE


def get_upload_extension(upload: UploadFile) -> str:
    filename = upload.filename or ""
    extension = Path(filename).suffix.lower().lstrip(".")

    if not extension and upload.content_type:
        guessed = mimetypes.guess_extension(upload.content_type)
        if guessed:
            extension = guessed.lstrip(".")

    if not extension:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not determine banner file extension",
        )

    return extension


def is_image_content_type(content_type: str | None) -> bool:
    return bool(content_type and content_type.startswith("image/"))


def ensure_document_upload(upload: UploadFile) -> None:
    content_type = upload.content_type or ""
    if is_image_content_type(content_type):
        return

    if content_type == "application/pdf":
        return

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Document file must be an image or PDF",
    )


def ensure_pdf_upload(upload: UploadFile) -> None:
    if upload.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attachment file must be a PDF",
        )


def ensure_upload_matches_role(upload: UploadFile, role: str | None) -> None:
    if role == BANNER_IMAGE_ROLE:
        ensure_image_upload(upload)
        return

    if role == ATTACHMENT_PDF_ROLE:
        ensure_pdf_upload(upload)
        return

    ensure_document_upload(upload)


def build_document_object_name(document_id: str, extension: str) -> str:
    normalized_extension = extension.lstrip(".")
    return f"{document_id}.{normalized_extension}"


def build_document_download_url(document_id: str) -> str:
    return f"/documents/{document_id}/download"


def ensure_image_upload(upload: UploadFile) -> None:
    if not is_image_content_type(upload.content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Banner file must be an image",
        )
