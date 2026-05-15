from __future__ import annotations

from fastapi import Depends

from src.dependencies.repositories import get_event_repository
from src.infra.repositories.event_repository import SqlModelEventRepository
from src.usecases.event import (
    CreateEventUseCase,
    DeleteEventUseCase,
    GetEventByIdUseCase,
    ListAllEventsUseCase,
    UpdateEventUseCase,
)


def get_create_event_usecase(
    event_repository: SqlModelEventRepository = Depends(get_event_repository),
) -> CreateEventUseCase:
    return CreateEventUseCase(event_repository)


def get_list_all_events_usecase(
    event_repository: SqlModelEventRepository = Depends(get_event_repository),
) -> ListAllEventsUseCase:
    return ListAllEventsUseCase(event_repository)


def get_get_event_by_id_usecase(
    event_repository: SqlModelEventRepository = Depends(get_event_repository),
) -> GetEventByIdUseCase:
    return GetEventByIdUseCase(event_repository)


def get_update_event_usecase(
    event_repository: SqlModelEventRepository = Depends(get_event_repository),
) -> UpdateEventUseCase:
    return UpdateEventUseCase(event_repository)


def get_delete_event_usecase(
    event_repository: SqlModelEventRepository = Depends(get_event_repository),
) -> DeleteEventUseCase:
    return DeleteEventUseCase(event_repository)
