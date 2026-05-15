from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any
from typing import Protocol

from fastapi_pagination import Params

from src.models.document import Document, DocumentCreate


class DocumentRepositoryProtocol(Protocol):
    def transaction(self) -> AsyncIterator[None]: ...

    async def create(self, data: DocumentCreate) -> Document: ...

    async def get_by_id(self, document_id: int) -> Document | None: ...

    async def list_by_event_id_paginated(self, event_id: int, params: Params) -> Any: ...

    async def update_size_bytes(self, document: Document, size_bytes: int) -> Document: ...

    async def update(self, document: Document, data) -> Document: ...

    async def delete(self, document: Document) -> None: ...
