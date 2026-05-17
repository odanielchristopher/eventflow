from __future__ import annotations

from fastapi import Depends

from src.dependencies.repositories import (
    get_activity_repository,
    get_check_in_repository,
    get_document_repository,
    get_event_repository,
    get_speaker_repository,
    get_subscription_repository,
)
from src.infra.repositories.activity_repository import SqlModelActivityRepository
from src.infra.repositories.checkin_repository import SqlModelCheckInRepository
from src.infra.repositories.document_repository import SqlModelDocumentRepository
from src.infra.repositories.event_repository import SqlModelEventRepository
from src.infra.repositories.speaker_repository import SqlModelSpeakerRepository
from src.infra.repositories.subscription_repository import SqlModelSubscriptionRepository
from src.usecases.activity import (
    CreateActivityUseCase,
    DeleteActivityUseCase,
    GetActivityByIdUseCase,
    ListActivitiesUseCase,
    UpdateActivityUseCase,
)
from src.usecases.checkin import (
    CreateCheckInUseCase,
    DeleteCheckInUseCase,
    GetCheckInByIdUseCase,
    ListCheckInsUseCase,
    UpdateCheckInUseCase,
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
    CreateEventUseCase,
    DeleteEventUseCase,
    GetEventByIdUseCase,
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


def get_create_speaker_usecase(
    speaker_repository: SqlModelSpeakerRepository = Depends(get_speaker_repository),
) -> CreateSpeakerUseCase:
    return CreateSpeakerUseCase(speaker_repository)


def get_list_speakers_usecase(
    speaker_repository: SqlModelSpeakerRepository = Depends(get_speaker_repository),
) -> ListSpeakersUseCase:
    return ListSpeakersUseCase(speaker_repository)


def get_speaker_by_id_usecase(
    speaker_repository: SqlModelSpeakerRepository = Depends(get_speaker_repository),
) -> GetSpeakerByIdUseCase:
    return GetSpeakerByIdUseCase(speaker_repository)


def get_update_speaker_usecase(
    speaker_repository: SqlModelSpeakerRepository = Depends(get_speaker_repository),
) -> UpdateSpeakerUseCase:
    return UpdateSpeakerUseCase(speaker_repository)


def get_delete_speaker_usecase(
    speaker_repository: SqlModelSpeakerRepository = Depends(get_speaker_repository),
) -> DeleteSpeakerUseCase:
    return DeleteSpeakerUseCase(speaker_repository)


def get_create_activity_usecase(
    event_repository: SqlModelEventRepository = Depends(get_event_repository),
    speaker_repository: SqlModelSpeakerRepository = Depends(get_speaker_repository),
    activity_repository: SqlModelActivityRepository = Depends(get_activity_repository),
) -> CreateActivityUseCase:
    return CreateActivityUseCase(
        event_repository,
        speaker_repository,
        activity_repository,
    )


def get_list_activities_usecase(
    event_repository: SqlModelEventRepository = Depends(get_event_repository),
    activity_repository: SqlModelActivityRepository = Depends(get_activity_repository),
) -> ListActivitiesUseCase:
    return ListActivitiesUseCase(event_repository, activity_repository)


def get_activity_by_id_usecase(
    activity_repository: SqlModelActivityRepository = Depends(get_activity_repository),
) -> GetActivityByIdUseCase:
    return GetActivityByIdUseCase(activity_repository)


def get_update_activity_usecase(
    event_repository: SqlModelEventRepository = Depends(get_event_repository),
    speaker_repository: SqlModelSpeakerRepository = Depends(get_speaker_repository),
    activity_repository: SqlModelActivityRepository = Depends(get_activity_repository),
) -> UpdateActivityUseCase:
    return UpdateActivityUseCase(
        event_repository,
        speaker_repository,
        activity_repository,
    )


def get_delete_activity_usecase(
    activity_repository: SqlModelActivityRepository = Depends(get_activity_repository),
) -> DeleteActivityUseCase:
    return DeleteActivityUseCase(activity_repository)


def get_create_check_in_usecase(
    subscription_repository: SqlModelSubscriptionRepository = Depends(
        get_subscription_repository,
    ),
    check_in_repository: SqlModelCheckInRepository = Depends(get_check_in_repository),
) -> CreateCheckInUseCase:
    return CreateCheckInUseCase(subscription_repository, check_in_repository)


def get_list_check_ins_usecase(
    event_repository: SqlModelEventRepository = Depends(get_event_repository),
    check_in_repository: SqlModelCheckInRepository = Depends(get_check_in_repository),
) -> ListCheckInsUseCase:
    return ListCheckInsUseCase(event_repository, check_in_repository)


def get_check_in_by_id_usecase(
    check_in_repository: SqlModelCheckInRepository = Depends(get_check_in_repository),
) -> GetCheckInByIdUseCase:
    return GetCheckInByIdUseCase(check_in_repository)


def get_update_check_in_usecase(
    subscription_repository: SqlModelSubscriptionRepository = Depends(
        get_subscription_repository,
    ),
    check_in_repository: SqlModelCheckInRepository = Depends(get_check_in_repository),
) -> UpdateCheckInUseCase:
    return UpdateCheckInUseCase(subscription_repository, check_in_repository)


def get_delete_check_in_usecase(
    check_in_repository: SqlModelCheckInRepository = Depends(get_check_in_repository),
) -> DeleteCheckInUseCase:
    return DeleteCheckInUseCase(check_in_repository)
