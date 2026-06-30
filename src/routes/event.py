from __future__ import annotations

from datetime import date as date_type
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, File, Response, UploadFile, status
from fastapi_pagination import Page, Params

from src.dependencies.usecases import (
    get_count_events_usecase,
    get_create_event_usecase,
    get_delete_event_usecase,
    get_get_event_by_id_usecase,
    get_list_events_by_subscription_price_range_usecase,
    get_list_all_events_usecase,
    get_update_event_usecase,
)
from src.models.event import EventCountRead, EventCreate, EventRead, EventUpdate
from src.usecases.event import (
    CountEventsUseCase,
    CreateEventUseCase,
    DeleteEventUseCase,
    GetEventByIdUseCase,
    ListEventsBySubscriptionPriceRangeUseCase,
    ListAllEventsUseCase,
    UpdateEventUseCase,
)


router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=Page[EventRead])
async def get_all_events(
    params: Params = Depends(),
    usecase: ListAllEventsUseCase = Depends(get_list_all_events_usecase),
):
    return await usecase.execute(params)


@router.get("/analytics/count", response_model=EventCountRead)
async def count_events(
    date_from: date_type | None = None,
    date_to: date_type | None = None,
    location: str | None = None,
    title: str | None = None,
    case_sensitive: bool = False,
    usecase: CountEventsUseCase = Depends(get_count_events_usecase),
):
    return await usecase.execute(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        case_sensitive=case_sensitive,
    )


@router.get("/analytics/by-subscription-price-range", response_model=Page[EventRead])
async def list_events_by_subscription_price_range(
    min_price: Decimal,
    max_price: Decimal,
    date_from: date_type | None = None,
    date_to: date_type | None = None,
    location: str | None = None,
    title: str | None = None,
    case_sensitive: bool = False,
    params: Params = Depends(),
    usecase: ListEventsBySubscriptionPriceRangeUseCase = Depends(
        get_list_events_by_subscription_price_range_usecase
    ),
):
    return await usecase.execute(
        params,
        min_price=min_price,
        max_price=max_price,
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        case_sensitive=case_sensitive,
    )


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED)
async def create_event(
    create_event_dto: Annotated[EventCreate, Depends(EventCreate.as_form)],
    banner_image: UploadFile = File(...),
    attachment_pdf: UploadFile = File(...),
    usecase: CreateEventUseCase = Depends(get_create_event_usecase),
):
    return await usecase.execute(create_event_dto, banner_image, attachment_pdf)


@router.get("/{event_id}", response_model=EventRead)
async def get_event_by_id(
    event_id: str,
    usecase: GetEventByIdUseCase = Depends(get_get_event_by_id_usecase),
):
    return await usecase.execute(event_id)


@router.put("/{event_id}", response_model=EventRead)
async def update_event(
    event_id: str,
    update_event_dto: Annotated[EventUpdate, Depends(EventUpdate.as_form)],
    banner_image: UploadFile | None = File(default=None),
    attachment_pdf: UploadFile | None = File(default=None),
    usecase: UpdateEventUseCase = Depends(get_update_event_usecase),
):
    return await usecase.execute(
        event_id,
        update_event_dto,
        banner_image=banner_image,
        attachment_pdf=attachment_pdf,
    )


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={204: {"description": "Event deleted successfully"}},
)
async def delete_event(
    event_id: str,
    usecase: DeleteEventUseCase = Depends(get_delete_event_usecase),
) -> Response:
    await usecase.execute(event_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
