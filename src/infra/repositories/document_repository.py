from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.document import Document, DocumentCreate, DocumentUpdate


class SqlModelDocumentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        async with self.session.begin():
            yield

    async def create(self, data: DocumentCreate) -> Document:
        document = Document.model_validate(data.model_dump())
        self.session.add(document)
        await self.session.flush()
        await self.session.refresh(document)
        return document

    async def get_by_id(self, document_id: int) -> Document | None:
        result = await self.session.execute(
            select(Document)
            .options(selectinload(Document.event))
            .where(Document.id == document_id)
        )
        return result.scalar_one_or_none()

    async def list_by_event_id(self, event_id: int) -> list[Document]:
        result = await self.session.execute(
            select(Document)
            .where(Document.event_id == event_id)
            .order_by(Document.created_at.desc(), Document.id.desc())
        )
        return list(result.scalars().all())

    async def update_size_bytes(self, document: Document, size_bytes: int) -> Document:
        document.size_bytes = size_bytes
        self.session.add(document)
        await self.session.flush()
        await self.session.refresh(document)
        return document

    async def update(self, document: Document, data: DocumentUpdate) -> Document:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(document, field, value)

        self.session.add(document)
        await self.session.flush()
        await self.session.refresh(document)
        return document

    async def delete(self, document: Document) -> None:
        await self.session.delete(document)
