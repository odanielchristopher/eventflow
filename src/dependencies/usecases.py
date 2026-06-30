from __future__ import annotations

from fastapi import Depends

from src.dependencies.repositories import (
    get_activity_repository,
    get_document_repository,
    get_event_repository,
    get_speaker_repository,
    get_subscription_repository,
)
from src.dependencies.storage import get_minio_storage_service
from src.infra.repositories.activity_repository import BeanieActivityRepository
from src.infra.repositories.document_repository import BeanieDocumentRepository
from src.infra.repositories.event_repository import BeanieEventRepository
from src.infra.repositories.speaker_repository import BeanieSpeakerRepository
from src.infra.repositories.subscription_repository import SqlModelSubscriptionRepository
from src.infra.storage import MinioStorageService
from src.usecases.activity import (
    CreateActivityUseCase,
    DeleteActivityUseCase,
    GetActivityByIdUseCase,
    ListActivitiesUseCase,
    UpdateActivityUseCase,
)
from src.usecases.document import (
    CreateDocumentUseCase,
    DeleteDocumentUseCase,
    DownloadDocumentUseCase,
    GetDocumentByIdUseCase,
    ListEventDocumentsUseCase,
    ReplaceDocumentUseCase,
)
from src.usecases.event import (
    CountEventsUseCase,
    CreateEventUseCase,
    DeleteEventUseCase,
    GetEventByIdUseCase,
    ListEventsBySubscriptionPriceRangeUseCase,
    ListAllEventsUseCase,
    UpdateEventUseCase,
)
from src.usecases.speaker import (
    CreateSpeakerUseCase,
    DeleteSpeakerUseCase,
    GetSpeakerByIdUseCase,
    ListSpeakersUseCase,
    UpdateSpeakerUseCase,
)
from src.usecases.subscription import (
    CountEventSubscriptionsCheckInUseCase,
    CreateSubscriptionUseCase,
    DeleteSubscriptionUseCase,
    GetEventAttendanceRateUseCase,
    GetSubscriptionByIdUseCase,
    ListEventSubscriptionsUseCase,
    UpdateSubscriptionUseCase,
)


def get_create_event_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    document_repository: BeanieDocumentRepository = Depends(get_document_repository),
    storage_service: MinioStorageService = Depends(get_minio_storage_service),
) -> CreateEventUseCase:
    return CreateEventUseCase(event_repository, document_repository, storage_service)


def get_list_all_events_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    document_repository: BeanieDocumentRepository = Depends(get_document_repository),
) -> ListAllEventsUseCase:
    return ListAllEventsUseCase(event_repository, document_repository)


def get_count_events_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
) -> CountEventsUseCase:
    return CountEventsUseCase(event_repository)


def get_list_events_by_subscription_price_range_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    document_repository: BeanieDocumentRepository = Depends(get_document_repository),
) -> ListEventsBySubscriptionPriceRangeUseCase:
    return ListEventsBySubscriptionPriceRangeUseCase(
        event_repository,
        document_repository,
    )


def get_get_event_by_id_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    document_repository: BeanieDocumentRepository = Depends(get_document_repository),
) -> GetEventByIdUseCase:
    return GetEventByIdUseCase(event_repository, document_repository)


def get_update_event_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    document_repository: BeanieDocumentRepository = Depends(get_document_repository),
    storage_service: MinioStorageService = Depends(get_minio_storage_service),
) -> UpdateEventUseCase:
    return UpdateEventUseCase(event_repository, document_repository, storage_service)


def get_delete_event_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    document_repository: BeanieDocumentRepository = Depends(get_document_repository),
    storage_service: MinioStorageService = Depends(get_minio_storage_service),
) -> DeleteEventUseCase:
    return DeleteEventUseCase(event_repository, document_repository, storage_service)


def get_create_document_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    document_repository: BeanieDocumentRepository = Depends(get_document_repository),
    storage_service: MinioStorageService = Depends(get_minio_storage_service),
) -> CreateDocumentUseCase:
    return CreateDocumentUseCase(event_repository, document_repository, storage_service)


def get_list_event_documents_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    document_repository: BeanieDocumentRepository = Depends(get_document_repository),
) -> ListEventDocumentsUseCase:
    return ListEventDocumentsUseCase(event_repository, document_repository)


def get_document_by_id_usecase(
    document_repository: BeanieDocumentRepository = Depends(get_document_repository),
) -> GetDocumentByIdUseCase:
    return GetDocumentByIdUseCase(document_repository)


def get_download_document_usecase(
    document_repository: BeanieDocumentRepository = Depends(get_document_repository),
    storage_service: MinioStorageService = Depends(get_minio_storage_service),
) -> DownloadDocumentUseCase:
    return DownloadDocumentUseCase(document_repository, storage_service)


def get_replace_document_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    document_repository: BeanieDocumentRepository = Depends(get_document_repository),
    storage_service: MinioStorageService = Depends(get_minio_storage_service),
) -> ReplaceDocumentUseCase:
    return ReplaceDocumentUseCase(event_repository, document_repository, storage_service)


def get_delete_document_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    document_repository: BeanieDocumentRepository = Depends(get_document_repository),
    storage_service: MinioStorageService = Depends(get_minio_storage_service),
) -> DeleteDocumentUseCase:
    return DeleteDocumentUseCase(event_repository, document_repository, storage_service)


def get_create_subscription_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    subscription_repository: SqlModelSubscriptionRepository = Depends(get_subscription_repository),
) -> CreateSubscriptionUseCase:
    return CreateSubscriptionUseCase(event_repository, subscription_repository)


def get_list_event_subscriptions_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    subscription_repository: SqlModelSubscriptionRepository = Depends(get_subscription_repository),
) -> ListEventSubscriptionsUseCase:
    return ListEventSubscriptionsUseCase(event_repository, subscription_repository)


def get_count_event_subscriptions_check_in_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    subscription_repository: SqlModelSubscriptionRepository = Depends(get_subscription_repository),
) -> CountEventSubscriptionsCheckInUseCase:
    return CountEventSubscriptionsCheckInUseCase(
        event_repository,
        subscription_repository,
    )


def get_event_attendance_rate_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    subscription_repository: SqlModelSubscriptionRepository = Depends(get_subscription_repository),
) -> GetEventAttendanceRateUseCase:
    return GetEventAttendanceRateUseCase(
        event_repository,
        subscription_repository,
    )


def get_subscription_by_id_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    subscription_repository: SqlModelSubscriptionRepository = Depends(get_subscription_repository),
) -> GetSubscriptionByIdUseCase:
    return GetSubscriptionByIdUseCase(event_repository, subscription_repository)


def get_update_subscription_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    subscription_repository: SqlModelSubscriptionRepository = Depends(get_subscription_repository),
) -> UpdateSubscriptionUseCase:
    return UpdateSubscriptionUseCase(event_repository, subscription_repository)


def get_delete_subscription_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    subscription_repository: SqlModelSubscriptionRepository = Depends(get_subscription_repository),
) -> DeleteSubscriptionUseCase:
    return DeleteSubscriptionUseCase(event_repository, subscription_repository)


def get_create_speaker_usecase(
    speaker_repository: BeanieSpeakerRepository = Depends(get_speaker_repository),
) -> CreateSpeakerUseCase:
    return CreateSpeakerUseCase(speaker_repository)


def get_list_speakers_usecase(
    speaker_repository: BeanieSpeakerRepository = Depends(get_speaker_repository),
) -> ListSpeakersUseCase:
    return ListSpeakersUseCase(speaker_repository)


def get_speaker_by_id_usecase(
    speaker_repository: BeanieSpeakerRepository = Depends(get_speaker_repository),
) -> GetSpeakerByIdUseCase:
    return GetSpeakerByIdUseCase(speaker_repository)


def get_update_speaker_usecase(
    speaker_repository: BeanieSpeakerRepository = Depends(get_speaker_repository),
) -> UpdateSpeakerUseCase:
    return UpdateSpeakerUseCase(speaker_repository)


def get_delete_speaker_usecase(
    speaker_repository: BeanieSpeakerRepository = Depends(get_speaker_repository),
) -> DeleteSpeakerUseCase:
    return DeleteSpeakerUseCase(speaker_repository)


def get_create_activity_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    speaker_repository: BeanieSpeakerRepository = Depends(get_speaker_repository),
    activity_repository: BeanieActivityRepository = Depends(get_activity_repository),
) -> CreateActivityUseCase:
    return CreateActivityUseCase(
        event_repository,
        speaker_repository,
        activity_repository,
    )


def get_list_activities_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    activity_repository: BeanieActivityRepository = Depends(get_activity_repository),
    speaker_repository: BeanieSpeakerRepository = Depends(get_speaker_repository),
) -> ListActivitiesUseCase:
    return ListActivitiesUseCase(
        event_repository,
        activity_repository,
        speaker_repository,
    )


def get_activity_by_id_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    activity_repository: BeanieActivityRepository = Depends(get_activity_repository),
    speaker_repository: BeanieSpeakerRepository = Depends(get_speaker_repository),
) -> GetActivityByIdUseCase:
    return GetActivityByIdUseCase(
        event_repository,
        activity_repository,
        speaker_repository,
    )


def get_update_activity_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    speaker_repository: BeanieSpeakerRepository = Depends(get_speaker_repository),
    activity_repository: BeanieActivityRepository = Depends(get_activity_repository),
) -> UpdateActivityUseCase:
    return UpdateActivityUseCase(
        event_repository,
        speaker_repository,
        activity_repository,
    )


def get_delete_activity_usecase(
    event_repository: BeanieEventRepository = Depends(get_event_repository),
    activity_repository: BeanieActivityRepository = Depends(get_activity_repository),
) -> DeleteActivityUseCase:
    return DeleteActivityUseCase(event_repository, activity_repository)
