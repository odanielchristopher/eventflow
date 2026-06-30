from __future__ import annotations

from datetime import time as time_type

from fastapi import APIRouter, Depends, Response, status
from fastapi_pagination import Page, Params

from src.dependencies.usecases import (
    get_activity_by_id_usecase,
    get_create_activity_usecase,
    get_delete_activity_usecase,
    get_list_activities_usecase,
    get_update_activity_usecase,
)
from src.models.activity import ActivityCreate, ActivityRead, ActivityUpdate
from src.usecases.activity import (
    CreateActivityUseCase,
    DeleteActivityUseCase,
    GetActivityByIdUseCase,
    ListActivitiesUseCase,
    UpdateActivityUseCase,
)


router = APIRouter(prefix="/events/{event_id}/activities", tags=["activities"])


@router.post("", response_model=ActivityRead, status_code=status.HTTP_201_CREATED)
async def create_activity(
    event_id: str,
    payload: ActivityCreate,
    usecase: CreateActivityUseCase = Depends(get_create_activity_usecase),
):
    return await usecase.execute(event_id, payload)


@router.get("", response_model=Page[ActivityRead])
async def list_activities(
    event_id: str,
    title: str | None = None,
    speaker_id: str | None = None,
    scheduled_from: time_type | None = None,
    scheduled_to: time_type | None = None,
    case_sensitive: bool = False,
    params: Params = Depends(),
    usecase: ListActivitiesUseCase = Depends(get_list_activities_usecase),
):
    return await usecase.execute(
        event_id,
        params,
        title=title,
        speaker_id=speaker_id,
        scheduled_from=scheduled_from,
        scheduled_to=scheduled_to,
        case_sensitive=case_sensitive,
    )


@router.get("/{activity_id}", response_model=ActivityRead)
async def get_activity_by_id(
    event_id: str,
    activity_id: str,
    usecase: GetActivityByIdUseCase = Depends(get_activity_by_id_usecase),
):
    return await usecase.execute(event_id, activity_id)


@router.put("/{activity_id}", response_model=ActivityRead)
async def update_activity(
    event_id: str,
    activity_id: str,
    payload: ActivityUpdate,
    usecase: UpdateActivityUseCase = Depends(get_update_activity_usecase),
):
    return await usecase.execute(event_id, activity_id, payload)


@router.delete(
    "/{activity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete_activity(
    event_id: str,
    activity_id: str,
    usecase: DeleteActivityUseCase = Depends(get_delete_activity_usecase),
) -> Response:
    await usecase.execute(event_id, activity_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
