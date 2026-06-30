from __future__ import annotations

from datetime import date as date_type

from fastapi import APIRouter, Depends, Response, status
from fastapi_pagination import Page, Params

from src.dependencies.usecases import (
    get_count_event_subscriptions_check_in_usecase,
    get_create_subscription_usecase,
    get_delete_subscription_usecase,
    get_list_event_subscriptions_usecase,
    get_subscription_by_id_usecase,
    get_update_subscription_usecase,
)
from src.models.subscription import (
    CheckInCreate,
    SubscriptionCheckInCountRead,
    SubscriptionCreate,
    SubscriptionRead,
    SubscriptionUpdate,
)
from src.usecases.subscription import (
    CountEventSubscriptionsCheckInUseCase,
    CreateSubscriptionUseCase,
    DeleteSubscriptionUseCase,
    GetSubscriptionByIdUseCase,
    ListEventSubscriptionsUseCase,
    UpdateSubscriptionUseCase,
)


router = APIRouter(prefix="/events/{event_id}/subscriptions", tags=["subscriptions"])


@router.post("", response_model=SubscriptionRead, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    event_id: str,
    payload: SubscriptionCreate,
    usecase: CreateSubscriptionUseCase = Depends(get_create_subscription_usecase),
):
    return await usecase.execute(event_id, payload)


@router.get("", response_model=Page[SubscriptionRead])
async def list_subscriptions(
    event_id: str,
    name: str | None = None,
    case_sensitive: bool = False,
    registered_from: date_type | None = None,
    registered_to: date_type | None = None,
    params: Params = Depends(),
    usecase: ListEventSubscriptionsUseCase = Depends(get_list_event_subscriptions_usecase),
):
    return await usecase.execute(
        event_id,
        params,
        name=name,
        case_sensitive=case_sensitive,
        registered_from=registered_from,
        registered_to=registered_to,
    )


@router.get("/check-ins/count", response_model=SubscriptionCheckInCountRead)
async def count_subscriptions_with_check_in(
    event_id: str,
    usecase: CountEventSubscriptionsCheckInUseCase = Depends(
        get_count_event_subscriptions_check_in_usecase,
    ),
):
    return await usecase.execute(event_id)


@router.get("/{subscription_id}", response_model=SubscriptionRead)
async def get_subscription_by_id(
    event_id: str,
    subscription_id: str,
    usecase: GetSubscriptionByIdUseCase = Depends(get_subscription_by_id_usecase),
):
    return await usecase.execute(event_id, subscription_id)


@router.post("/{subscription_id}", response_model=SubscriptionRead)
async def create_subscription_check_in(
    event_id: str,
    subscription_id: str,
    payload: CheckInCreate,
    usecase: UpdateSubscriptionUseCase = Depends(get_update_subscription_usecase),
):
    return await usecase.execute(
        event_id,
        subscription_id,
        SubscriptionUpdate(check_in=payload),
    )


@router.patch("/{subscription_id}", response_model=SubscriptionRead)
async def update_subscription(
    event_id: str,
    subscription_id: str,
    payload: SubscriptionUpdate,
    usecase: UpdateSubscriptionUseCase = Depends(get_update_subscription_usecase),
):
    return await usecase.execute(event_id, subscription_id, payload)


@router.delete(
    "/{subscription_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete_subscription(
    event_id: str,
    subscription_id: str,
    check_in_only: bool = False,
    usecase: DeleteSubscriptionUseCase = Depends(get_delete_subscription_usecase),
    update_usecase: UpdateSubscriptionUseCase = Depends(get_update_subscription_usecase),
) -> Response:
    if check_in_only:
        await update_usecase.execute(
            event_id,
            subscription_id,
            SubscriptionUpdate(check_in=None),
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    await usecase.execute(event_id, subscription_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
