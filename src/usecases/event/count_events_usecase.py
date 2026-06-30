from __future__ import annotations

from datetime import date as date_type

from src.contracts.event_repository import EventRepositoryProtocol
from src.models.event import EventCountRead


class CountEventsUseCase:
    def __init__(self, event_repository: EventRepositoryProtocol) -> None:
        self.event_repository = event_repository

    async def execute(
        self,
        *,
        date_from: date_type | None = None,
        date_to: date_type | None = None,
        location: str | None = None,
        title: str | None = None,
        case_sensitive: bool = False,
    ) -> EventCountRead:
        count = await self.event_repository.count_filtered(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            case_sensitive=case_sensitive,
        )
        return EventCountRead(count=count)
