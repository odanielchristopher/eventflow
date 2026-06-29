from __future__ import annotations

from typing import Any

from fastapi_pagination import Params, create_page

from src.contracts.document_repository import DocumentRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol
from src.usecases.event.presentation import group_documents_by_event_id, serialize_event

class ListAllEventsUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        document_repository: DocumentRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.document_repository = document_repository

    async def execute(self, params: Params) -> Any:
        page = await self.event_repository.list_paginated(params)
        event_ids = [str(event.id) for event in page.items]
        documents = await self.document_repository.list_by_event_ids(event_ids)
        documents_by_event_id = group_documents_by_event_id(documents)

        items = [
            serialize_event(event, documents_by_event_id.get(str(event.id), []))
            for event in page.items
        ]
        return create_page(items, total=page.total, params=params)
