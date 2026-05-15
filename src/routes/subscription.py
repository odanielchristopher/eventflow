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


router = APIRouter(tags=["subscriptions"])


@router.post("/subscriptions", response_model=SubscriptionRead, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    payload: SubscriptionCreate,
    usecase: CreateSubscriptionUseCase = Depends(get_create_subscription_usecase),
):
    return await usecase.execute(payload)


@router.get("/subscriptions", response_model=Page[SubscriptionRead])
async def list_subscriptions(
    params: Params = Depends(),
    event_id: int | None = None,
    usecase: ListEventSubscriptionsUseCase = Depends(get_list_event_subscriptions_usecase),
):
    return await usecase.execute(params, event_id)


@router.get("/subscriptions/{subscription_id}", response_model=SubscriptionRead)
async def get_subscription_by_id(
    subscription_id: int,
    usecase: GetSubscriptionByIdUseCase = Depends(get_subscription_by_id_usecase),
):
    return await usecase.execute(subscription_id)


@router.put("/subscriptions/{subscription_id}", response_model=SubscriptionRead)
async def update_subscription(
    subscription_id: int,
    payload: SubscriptionUpdate,
    usecase: UpdateSubscriptionUseCase = Depends(get_update_subscription_usecase),
):
    return await usecase.execute(subscription_id, payload)


@router.delete(
    "/subscriptions/{subscription_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete_subscription(
    subscription_id: int,
    usecase: DeleteSubscriptionUseCase = Depends(get_delete_subscription_usecase),
) -> Response:
    await usecase.execute(subscription_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
