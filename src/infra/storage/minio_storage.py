from __future__ import annotations

import asyncio
from io import BytesIO
from urllib.parse import urlparse

from fastapi import UploadFile
from minio import Minio
from minio.error import S3Error

from src.core.config import get_settings


class MinioStorageService:
    def __init__(self) -> None:
        settings = get_settings()
        parsed_endpoint = self._parse_endpoint(settings.minio_endpoint)
        secure = settings.minio_secure or parsed_endpoint.scheme == "https"

        self.bucket = settings.minio_bucket
        self.client = Minio(
            parsed_endpoint.netloc,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=secure,
        )

    @staticmethod
    def _parse_endpoint(endpoint: str):
        normalized = endpoint if "://" in endpoint else f"http://{endpoint}"
        return urlparse(normalized)

    async def ensure_bucket_exists(self) -> None:
        await asyncio.to_thread(self._ensure_bucket_exists_sync)

    def _ensure_bucket_exists_sync(self) -> None:
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    async def upload_file(self, upload: UploadFile, object_name: str) -> int:
        content = await upload.read()
        await asyncio.to_thread(
            self._put_object_sync,
            object_name,
            content,
            upload.content_type or "application/octet-stream",
        )
        return len(content)

    def _put_object_sync(self, object_name: str, content: bytes, content_type: str) -> None:
        self.client.put_object(
            self.bucket,
            object_name,
            data=BytesIO(content),
            length=len(content),
            content_type=content_type,
        )

    async def download_file(self, object_name: str) -> bytes:
        return await asyncio.to_thread(self._download_file_sync, object_name)

    def _download_file_sync(self, object_name: str) -> bytes:
        response = self.client.get_object(self.bucket, object_name)
        try:
            return response.read()
        finally:
            response.close()
            response.release_conn()

    async def delete_file(self, object_name: str) -> None:
        await asyncio.to_thread(self._delete_file_sync, object_name)

    def _delete_file_sync(self, object_name: str) -> None:
        try:
            self.client.remove_object(self.bucket, object_name)
        except S3Error as exc:
            if exc.code != "NoSuchKey":
                raise
