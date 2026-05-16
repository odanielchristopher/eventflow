from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from fastapi_pagination import Page, Params

from src.dependencies.usecases import (
    get_create_speaker_usecase,
    get_delete_speaker_usecase,
    get_speaker_by_id_usecase,
    get_list_speakers_usecase,
    get_update_speaker_usecase,
)
from src.models.speaker import SpeakerCreate, SpeakerRead, SpeakerUpdate
from src.usecases.speaker import (
    CreateSpeakerUseCase,
    DeleteSpeakerUseCase,
    GetSpeakerByIdUseCase,
    ListSpeakersUseCase,
    UpdateSpeakerUseCase,
)


router = APIRouter(prefix="/speakers", tags=["speakers"])


@router.post("", response_model=SpeakerRead, status_code=status.HTTP_201_CREATED)
async def create_speaker(
    payload: SpeakerCreate,
    usecase: CreateSpeakerUseCase = Depends(get_create_speaker_usecase),
):
    return await usecase.execute(payload)


@router.get("", response_model=Page[SpeakerRead])
async def list_speakers(
    params: Params = Depends(),
    usecase: ListSpeakersUseCase = Depends(get_list_speakers_usecase),
):
    return await usecase.execute(params)


@router.get("/{speaker_id}", response_model=SpeakerRead)
async def get_speaker_by_id(
    speaker_id: int,
    usecase: GetSpeakerByIdUseCase = Depends(get_speaker_by_id_usecase),
):
    return await usecase.execute(speaker_id)


@router.put("/{speaker_id}", response_model=SpeakerRead)
async def update_speaker(
    speaker_id: int,
    payload: SpeakerUpdate,
    usecase: UpdateSpeakerUseCase = Depends(get_update_speaker_usecase),
):
    return await usecase.execute(speaker_id, payload)


@router.delete(
    "/{speaker_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete_speaker(
    speaker_id: int,
    usecase: DeleteSpeakerUseCase = Depends(get_delete_speaker_usecase),
) -> Response:
    await usecase.execute(speaker_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
