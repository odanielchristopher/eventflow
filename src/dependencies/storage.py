from __future__ import annotations

from functools import lru_cache

from src.infra.storage import MinioStorageService


@lru_cache(maxsize=1)
def get_minio_storage_service() -> MinioStorageService:
    return MinioStorageService()
