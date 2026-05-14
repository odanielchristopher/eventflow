from __future__ import annotations

from src.models.paginated_data import PaginatedData
from src.models.event.event import Event

ListEventsResponse = PaginatedData[Event]
