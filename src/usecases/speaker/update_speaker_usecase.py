from __future__ import annotations

from fastapi import HTTPException

from src.contracts.speaker_repository import SpeakerRepositoryProtocol
from src.models.speaker import Speaker, SpeakerUpdate


class UpdateSpeakerUseCase:
    def __init__(self, speaker_repository: SpeakerRepositoryProtocol) -> None:
        self.speaker_repository = speaker_repository

    async def execute(self, speaker_id: int, data: SpeakerUpdate) -> Speaker:
        async with self.speaker_repository.transaction():
            speaker = await self.speaker_repository.get_by_id(speaker_id)
            if speaker is None:
                raise HTTPException(status_code=404, detail="Speaker not found")

            return await self.speaker_repository.update(speaker, data)
