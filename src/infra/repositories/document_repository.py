from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from beanie import PydanticObjectId
from fastapi import HTTPException
from fastapi_pagination import Params, create_page

from src.models.document import Document, DocumentCreate, DocumentRole, DocumentUpdate


class BeanieDocumentRepository:
    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        yield

    async def create(self, data: DocumentCreate) -> Document:
        document = Document(**data.model_dump())
        await document.insert()
        return document

    async def get_by_id(self, document_id: str) -> Document | None:
        try:
            return await Document.get(PydanticObjectId(document_id))
        except Exception as exc:
            raise HTTPException(status_code=422, detail="Invalid document id") from exc

    async def list_by_event_id_paginated(self, event_id: str, params: Params) -> Any:
        query = Document.find({"event_id": event_id}).sort("-created_at", "-_id")
        total = await query.count()
        items = await query.skip((params.page - 1) * params.size).limit(params.size).to_list()
        return create_page(items, total=total, params=params)

    async def list_by_event_ids(self, event_ids: list[str]) -> list[Document]:
        if not event_ids:
            return []

        return await Document.find({"event_id": {"$in": event_ids}}).sort("-created_at", "-_id").to_list()

    async def get_by_event_id_and_role(
        self,
        event_id: str,
        role: DocumentRole,
    ) -> Document | None:
        return await Document.find_one({"event_id": event_id, "role": role})

    async def update_size_bytes(self, document: Document, size_bytes: int) -> Document:
        document.size_bytes = size_bytes
        await document.save()
        return document

    async def update(self, document: Document, data: DocumentUpdate) -> Document:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(document, field, value)

        await document.save()
        return document

    async def delete(self, document: Document) -> None:
        await document.delete()
