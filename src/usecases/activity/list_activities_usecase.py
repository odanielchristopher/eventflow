from __future__ import annotations

from datetime import time as time_type
from typing import Any

from fastapi import HTTPException
from fastapi_pagination import Params, create_page

from src.contracts.activity_repository import ActivityRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol
from src.contracts.speaker_repository import SpeakerRepositoryProtocol
from src.usecases.activity.presentation import (
    collect_speaker_ids,
    group_speakers_by_id,
    serialize_activity,
)


class ListActivitiesUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        activity_repository: ActivityRepositoryProtocol,
        speaker_repository: SpeakerRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.activity_repository = activity_repository
        self.speaker_repository = speaker_repository

    async def execute(
        self,
        event_id: str,
        params: Params,
        *,
        title: str | None = None,
        speaker_id: str | None = None,
        scheduled_from: time_type | None = None,
        scheduled_to: time_type | None = None,
        case_sensitive: bool = False,
    ) -> Any:
        event = await self.event_repository.get_by_id(event_id)
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")

        page = await self.activity_repository.list_paginated(
            params,
            event_id,
            title=title,
            speaker_id=speaker_id,
            scheduled_from=scheduled_from,
            scheduled_to=scheduled_to,
            case_sensitive=case_sensitive,
        )
        speaker_ids = collect_speaker_ids(page.items)
        speakers = await self.speaker_repository.list_by_ids(speaker_ids)
        speakers_by_id = group_speakers_by_id(speakers)
        items = [
            serialize_activity(
                activity,
                [
                    speakers_by_id[speaker_id]
                    for speaker_id in activity.speaker_ids
                    if speaker_id in speakers_by_id
                ],
            )
            for activity in page.items
        ]
        return create_page(items, total=page.total, params=params)
