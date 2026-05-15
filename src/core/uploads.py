from __future__ import annotations

import mimetypes
from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from src.core.config import get_settings


settings = get_settings()


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


def ensure_image_upload(upload: UploadFile) -> None:
    if not upload.content_type or not upload.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Banner file must be an image",
        )


def build_document_filename(document_id: int, extension: str) -> str:
    return f"{document_id}.{extension}"


def build_document_url(document_id: int, extension: str) -> str:
    return f"/uploads/{build_document_filename(document_id, extension)}"


async def save_upload_file(upload: UploadFile, filename: str) -> int:
    settings.resolved_upload_dir.mkdir(parents=True, exist_ok=True)
    destination = settings.resolved_upload_dir / filename
    content = await upload.read()
    destination.write_bytes(content)
    return len(content)


def delete_upload_by_url(file_url: str | None) -> None:
    if not file_url or not file_url.startswith("/uploads/"):
        return

    filename = file_url.removeprefix("/uploads/")
    path = settings.resolved_upload_dir / filename
    if path.exists():
        path.unlink()
