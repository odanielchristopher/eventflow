from __future__ import annotations

from typing import Generic, TypeVar

from src.models.base import BaseModel

T = TypeVar("T")


class PaginationMeta(BaseModel):
    total: int
    page: int
    per_page: int


class PaginatedData(BaseModel, Generic[T]):
    data: list[T]
    meta: PaginationMeta
