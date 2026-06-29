from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any
from typing import Protocol

from fastapi_pagination import Params

from src.models.document import Document, DocumentCreate, DocumentUpdate


class DocumentRepositoryProtocol(Protocol):
    def transaction(self) -> AsyncIterator[None]: ...

    async def create(self, data: DocumentCreate) -> Document: ...

    async def get_by_id(self, document_id: str) -> Document | None: ...

    async def list_by_event_id_paginated(self, event_id: str, params: Params) -> Any: ...

    async def list_by_event_ids(self, event_ids: list[str]) -> list[Document]: ...

    async def update_size_bytes(self, document: Document, size_bytes: int) -> Document: ...

    async def update(self, document: Document, data: DocumentUpdate) -> Document: ...

    async def delete(self, document: Document) -> None: ...
