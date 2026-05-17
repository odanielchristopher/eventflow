from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from fastapi_pagination import Page, Params

from src.dependencies.usecases import (
    get_create_subscription_usecase,
    get_delete_subscription_usecase,
    get_list_event_subscriptions_usecase,
    get_subscription_by_id_usecase,
    get_update_subscription_usecase,
)
from src.models.subscription import (
    SubscriptionCreate,
    SubscriptionRead,
    SubscriptionUpdate,
)
from src.usecases.subscription import (
    CreateSubscriptionUseCase,
    DeleteSubscriptionUseCase,
    GetSubscriptionByIdUseCase,
    ListEventSubscriptionsUseCase,
    UpdateSubscriptionUseCase,
)


router = APIRouter(prefix="/events/{event_id}/subscriptions", tags=["subscriptions"])


@router.post("", response_model=SubscriptionRead, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    event_id: int,
    payload: SubscriptionCreate,
    usecase: CreateSubscriptionUseCase = Depends(get_create_subscription_usecase),
):
    return await usecase.execute(event_id, payload)


@router.get("", response_model=Page[SubscriptionRead])
async def list_subscriptions(
    event_id: int,
    params: Params = Depends(),
    usecase: ListEventSubscriptionsUseCase = Depends(get_list_event_subscriptions_usecase),
):
    return await usecase.execute(event_id, params)


@router.get("/{subscription_id}", response_model=SubscriptionRead)
async def get_subscription_by_id(
    event_id: int,
    subscription_id: int,
    usecase: GetSubscriptionByIdUseCase = Depends(get_subscription_by_id_usecase),
):
    return await usecase.execute(event_id, subscription_id)


@router.put("/{subscription_id}", response_model=SubscriptionRead)
async def update_subscription(
    event_id: int,
    subscription_id: int,
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
    event_id: int,
    subscription_id: int,
    usecase: DeleteSubscriptionUseCase = Depends(get_delete_subscription_usecase),
) -> Response:
    await usecase.execute(event_id, subscription_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
