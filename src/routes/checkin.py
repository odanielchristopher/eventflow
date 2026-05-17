from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from fastapi_pagination import Page, Params

from src.dependencies.usecases import (
    get_check_in_by_id_usecase,
    get_create_check_in_usecase,
    get_delete_check_in_usecase,
    get_list_check_ins_usecase,
    get_update_check_in_usecase,
)
from src.models.checkin import CheckInCreate, CheckInRead, CheckInUpdate
from src.usecases.checkin import (
    CreateCheckInUseCase,
    DeleteCheckInUseCase,
    GetCheckInByIdUseCase,
    ListCheckInsUseCase,
    UpdateCheckInUseCase,
)


router = APIRouter(prefix="/check-ins", tags=["check-ins"])


@router.post("", response_model=CheckInRead, status_code=status.HTTP_201_CREATED)
async def create_check_in(
    payload: CheckInCreate,
    usecase: CreateCheckInUseCase = Depends(get_create_check_in_usecase),
):
    return await usecase.execute(payload)


@router.get("", response_model=Page[CheckInRead])
async def list_check_ins(
    params: Params = Depends(),
    event_id: int | None = None,
    usecase: ListCheckInsUseCase = Depends(get_list_check_ins_usecase),
):
    return await usecase.execute(params, event_id)


@router.get("/{check_in_id}", response_model=CheckInRead)
async def get_check_in_by_id(
    check_in_id: int,
    usecase: GetCheckInByIdUseCase = Depends(get_check_in_by_id_usecase),
):
    return await usecase.execute(check_in_id)


@router.put("/{check_in_id}", response_model=CheckInRead)
async def update_check_in(
    check_in_id: int,
    payload: CheckInUpdate,
    usecase: UpdateCheckInUseCase = Depends(get_update_check_in_usecase),
):
    return await usecase.execute(check_in_id, payload)


@router.delete(
    "/{check_in_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete_check_in(
    check_in_id: int,
    usecase: DeleteCheckInUseCase = Depends(get_delete_check_in_usecase),
) -> Response:
    await usecase.execute(check_in_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
