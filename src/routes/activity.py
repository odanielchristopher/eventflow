from __future__ import annotations

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


router = APIRouter(prefix="/activities", tags=["activities"])


@router.post("", response_model=ActivityRead, status_code=status.HTTP_201_CREATED)
async def create_activity(
    payload: ActivityCreate,
    usecase: CreateActivityUseCase = Depends(get_create_activity_usecase),
):
    return await usecase.execute(payload)


@router.get("", response_model=Page[ActivityRead])
async def list_activities(
    params: Params = Depends(),
    event_id: int | None = None,
    usecase: ListActivitiesUseCase = Depends(get_list_activities_usecase),
):
    return await usecase.execute(params, event_id)


@router.get("/{activity_id}", response_model=ActivityRead)
async def get_activity_by_id(
    activity_id: int,
    usecase: GetActivityByIdUseCase = Depends(get_activity_by_id_usecase),
):
    return await usecase.execute(activity_id)


@router.put("/{activity_id}", response_model=ActivityRead)
async def update_activity(
    activity_id: int,
    payload: ActivityUpdate,
    usecase: UpdateActivityUseCase = Depends(get_update_activity_usecase),
):
    return await usecase.execute(activity_id, payload)


@router.delete(
    "/{activity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete_activity(
    activity_id: int,
    usecase: DeleteActivityUseCase = Depends(get_delete_activity_usecase),
) -> Response:
    await usecase.execute(activity_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
