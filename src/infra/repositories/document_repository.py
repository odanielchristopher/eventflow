from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.document import Document, DocumentCreate


class SqlModelDocumentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: DocumentCreate) -> Document:
        document = Document.model_validate(data.model_dump())
        self.session.add(document)
        await self.session.commit()
        await self.session.refresh(document)
        return document

    async def get_by_id(self, document_id: int) -> Document | None:
        result = await self.session.execute(
            select(Document).where(Document.id == document_id)
        )
        return result.scalar_one_or_none()

    async def update_size_bytes(self, document: Document, size_bytes: int) -> Document:
        document.size_bytes = size_bytes
        self.session.add(document)
        await self.session.commit()
        await self.session.refresh(document)
        return document

    async def delete(self, document: Document) -> None:
        await self.session.delete(document)
        await self.session.commit()
