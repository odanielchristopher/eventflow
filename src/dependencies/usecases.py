from __future__ import annotations

from fastapi import Depends

from src.dependencies.repositories import (
    get_document_repository,
    get_event_repository,
    get_subscription_repository,
)
from src.infra.repositories.document_repository import SqlModelDocumentRepository
from src.infra.repositories.event_repository import SqlModelEventRepository
from src.infra.repositories.subscription_repository import SqlModelSubscriptionRepository
from src.usecases.document import (
    CreateDocumentUseCase,
    DeleteDocumentUseCase,
    DownloadDocumentUseCase,
    GetDocumentByIdUseCase,
    ListEventDocumentsUseCase,
    ReplaceDocumentUseCase,
)
from src.usecases.event import (
    CreateEventUseCase,
    DeleteEventUseCase,
    GetEventByIdUseCase,
    ListAllEventsUseCase,
    UpdateEventUseCase,
)
from src.usecases.subscription import (
    CreateSubscriptionUseCase,
    DeleteSubscriptionUseCase,
    GetSubscriptionByIdUseCase,
    ListEventSubscriptionsUseCase,
    UpdateSubscriptionUseCase,
)


def get_create_event_usecase(
    event_repository: SqlModelEventRepository = Depends(get_event_repository),
    document_repository: SqlModelDocumentRepository = Depends(get_document_repository),
) -> CreateEventUseCase:
    return CreateEventUseCase(event_repository, document_repository)


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
    document_repository: SqlModelDocumentRepository = Depends(get_document_repository),
) -> UpdateEventUseCase:
    return UpdateEventUseCase(event_repository, document_repository)


def get_delete_event_usecase(
    event_repository: SqlModelEventRepository = Depends(get_event_repository),
) -> DeleteEventUseCase:
    return DeleteEventUseCase(event_repository)


def get_create_document_usecase(
    event_repository: SqlModelEventRepository = Depends(get_event_repository),
    document_repository: SqlModelDocumentRepository = Depends(get_document_repository),
) -> CreateDocumentUseCase:
    return CreateDocumentUseCase(event_repository, document_repository)


def get_list_event_documents_usecase(
    event_repository: SqlModelEventRepository = Depends(get_event_repository),
    document_repository: SqlModelDocumentRepository = Depends(get_document_repository),
) -> ListEventDocumentsUseCase:
    return ListEventDocumentsUseCase(event_repository, document_repository)


def get_document_by_id_usecase(
    document_repository: SqlModelDocumentRepository = Depends(get_document_repository),
) -> GetDocumentByIdUseCase:
    return GetDocumentByIdUseCase(document_repository)


def get_download_document_usecase(
    document_repository: SqlModelDocumentRepository = Depends(get_document_repository),
) -> DownloadDocumentUseCase:
    return DownloadDocumentUseCase(document_repository)


def get_replace_document_usecase(
    event_repository: SqlModelEventRepository = Depends(get_event_repository),
    document_repository: SqlModelDocumentRepository = Depends(get_document_repository),
) -> ReplaceDocumentUseCase:
    return ReplaceDocumentUseCase(event_repository, document_repository)


def get_delete_document_usecase(
    event_repository: SqlModelEventRepository = Depends(get_event_repository),
    document_repository: SqlModelDocumentRepository = Depends(get_document_repository),
) -> DeleteDocumentUseCase:
    return DeleteDocumentUseCase(event_repository, document_repository)


def get_create_subscription_usecase(
    event_repository: SqlModelEventRepository = Depends(get_event_repository),
    subscription_repository: SqlModelSubscriptionRepository = Depends(get_subscription_repository),
) -> CreateSubscriptionUseCase:
    return CreateSubscriptionUseCase(event_repository, subscription_repository)


def get_list_event_subscriptions_usecase(
    event_repository: SqlModelEventRepository = Depends(get_event_repository),
    subscription_repository: SqlModelSubscriptionRepository = Depends(get_subscription_repository),
) -> ListEventSubscriptionsUseCase:
    return ListEventSubscriptionsUseCase(event_repository, subscription_repository)


def get_subscription_by_id_usecase(
    subscription_repository: SqlModelSubscriptionRepository = Depends(get_subscription_repository),
) -> GetSubscriptionByIdUseCase:
    return GetSubscriptionByIdUseCase(subscription_repository)


def get_update_subscription_usecase(
    event_repository: SqlModelEventRepository = Depends(get_event_repository),
    subscription_repository: SqlModelSubscriptionRepository = Depends(get_subscription_repository),
) -> UpdateSubscriptionUseCase:
    return UpdateSubscriptionUseCase(event_repository, subscription_repository)


def get_delete_subscription_usecase(
    subscription_repository: SqlModelSubscriptionRepository = Depends(get_subscription_repository),
) -> DeleteSubscriptionUseCase:
    return DeleteSubscriptionUseCase(subscription_repository)
