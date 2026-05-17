from __future__ import annotations

from fastapi import HTTPException

from src.contracts.activity_repository import ActivityRepositoryProtocol
from src.contracts.event_repository import EventRepositoryProtocol
from src.contracts.speaker_repository import SpeakerRepositoryProtocol
from src.models.activity import Activity, ActivityUpdate
from src.models.speaker import Speaker


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

    async def _get_speakers_or_raise(self, speaker_ids: list[int]) -> list[Speaker]:
        unique_speaker_ids = list(dict.fromkeys(speaker_ids))
        speakers = await self.speaker_repository.list_by_ids(unique_speaker_ids)
        found_ids = {speaker.id for speaker in speakers}
        if any(speaker_id not in found_ids for speaker_id in unique_speaker_ids):
            raise HTTPException(status_code=404, detail="Speaker not found")

        return speakers

    async def execute(self, activity_id: int, data: ActivityUpdate) -> Activity:
        async with self.activity_repository.transaction():
            activity = await self.activity_repository.get_by_id(activity_id)
            if activity is None:
                raise HTTPException(status_code=404, detail="Activity not found")

            next_event_id = data.event_id if data.event_id is not None else activity.event_id
            event = await self.event_repository.get_by_id(next_event_id)
            if event is None:
                raise HTTPException(status_code=404, detail="Event not found")

            speakers = None
            if data.speaker_ids is not None:
                speakers = await self._get_speakers_or_raise(data.speaker_ids)

            return await self.activity_repository.update(activity, data, speakers)
