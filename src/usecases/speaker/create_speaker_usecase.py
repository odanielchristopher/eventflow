from __future__ import annotations

from src.contracts.speaker_repository import SpeakerRepositoryProtocol
from src.models.speaker import Speaker, SpeakerCreate


class CreateSpeakerUseCase:
    def __init__(self, speaker_repository: SpeakerRepositoryProtocol) -> None:
        self.speaker_repository = speaker_repository

    async def execute(self, data: SpeakerCreate) -> Speaker:
        async with self.speaker_repository.transaction():
            return await self.speaker_repository.create(data)
