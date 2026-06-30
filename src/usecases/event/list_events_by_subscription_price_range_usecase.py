from __future__ import annotations

from datetime import date as date_type
from decimal import Decimal

from fastapi import HTTPException
from fastapi_pagination import Page, Params, create_page

from src.contracts.document_repository import DocumentRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol
from src.models.event import EventRead
from src.usecases.event.presentation import group_documents_by_event_id, serialize_event


class ListEventsBySubscriptionPriceRangeUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        document_repository: DocumentRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.document_repository = document_repository

    async def execute(
        self,
        params: Params,
        *,
        min_price: Decimal,
        max_price: Decimal,
        date_from: date_type | None = None,
        date_to: date_type | None = None,
        location: str | None = None,
        title: str | None = None,
        case_sensitive: bool = False,
    ) -> Page[EventRead]:
        if min_price > max_price:
            raise HTTPException(
                status_code=400,
                detail="min_price must be less than or equal to max_price",
            )

        page = await self.event_repository.list_by_subscription_price_range(
            params,
            min_price=min_price,
            max_price=max_price,
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            case_sensitive=case_sensitive,
        )
        event_ids = [str(event.id) for event in page.items]
        documents = await self.document_repository.list_by_event_ids(event_ids)
        documents_by_event_id = group_documents_by_event_id(documents)
        items = [
            serialize_event(event, documents_by_event_id.get(str(event.id), []))
            for event in page.items
        ]
        return create_page(items, total=page.total, params=params)
