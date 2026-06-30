from __future__ import annotations

from fastapi import HTTPException

from src.contracts.activity_repository import ActivityRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol
from src.contracts.speaker_repository import SpeakerRepositoryProtocol
from src.models.activity import ActivityRead
from src.usecases.activity.presentation import group_speakers_by_id, serialize_activity


class GetActivityByIdUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        activity_repository: ActivityRepositoryProtocol,
        speaker_repository: SpeakerRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.activity_repository = activity_repository
        self.speaker_repository = speaker_repository

    async def execute(self, event_id: str, activity_id: str) -> ActivityRead:
        event = await self.event_repository.get_by_id(event_id)
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")

        activity = await self.activity_repository.get_by_id(activity_id)
        if activity is None or activity.event_id != event_id:
            raise HTTPException(status_code=404, detail="Activity not found")

        speakers = await self.speaker_repository.list_by_ids(activity.speaker_ids)
        speakers_by_id = group_speakers_by_id(speakers)
        ordered_speakers = [
            speakers_by_id[speaker_id]
            for speaker_id in activity.speaker_ids
            if speaker_id in speakers_by_id
        ]
        return serialize_activity(activity, ordered_speakers)
