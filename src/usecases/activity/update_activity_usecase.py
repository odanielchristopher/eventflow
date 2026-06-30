from __future__ import annotations

from fastapi import HTTPException

from src.contracts.activity_repository import ActivityRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol
from src.contracts.speaker_repository import SpeakerRepositoryProtocol
from src.models.activity import ActivityRead, ActivityUpdate
from src.models.speaker import Speaker
from src.usecases.activity.presentation import group_speakers_by_id, serialize_activity


class UpdateActivityUseCase:
    def __init__(
        self,
        event_repository: EventRepositoryProtocol,
        speaker_repository: SpeakerRepositoryProtocol,
        activity_repository: ActivityRepositoryProtocol,
    ) -> None:
        self.event_repository = event_repository
        self.speaker_repository = speaker_repository
        self.activity_repository = activity_repository

    async def _get_speakers_or_raise(self, speaker_ids: list[str]) -> list[Speaker]:
        unique_speaker_ids = list(dict.fromkeys(speaker_ids))
        speakers = await self.speaker_repository.list_by_ids(unique_speaker_ids)
        found_ids = {str(speaker.id) for speaker in speakers}
        if any(speaker_id not in found_ids for speaker_id in unique_speaker_ids):
            raise HTTPException(status_code=404, detail="Speaker not found")

        return speakers

    async def execute(self, event_id: str, activity_id: str, data: ActivityUpdate) -> ActivityRead:
        async with self.activity_repository.transaction():
            event = await self.event_repository.get_by_id(event_id)
            if event is None:
                raise HTTPException(status_code=404, detail="Event not found")

            activity = await self.activity_repository.get_by_id(activity_id)
            if activity is None or activity.event_id != event_id:
                raise HTTPException(status_code=404, detail="Activity not found")

            speakers = None
            if data.speaker_ids is not None:
                speakers = await self._get_speakers_or_raise(data.speaker_ids)

            activity = await self.activity_repository.update(activity, data)
            if speakers is None:
                speakers = await self.speaker_repository.list_by_ids(activity.speaker_ids)

            speakers_by_id = group_speakers_by_id(speakers)
            ordered_speakers = [
                speakers_by_id[speaker_id]
                for speaker_id in activity.speaker_ids
                if speaker_id in speakers_by_id
            ]
            return serialize_activity(activity, ordered_speakers)
