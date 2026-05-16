from __future__ import annotations

from typing import Any

from fastapi_pagination import Params

from src.contracts.speaker_repository import SpeakerRepositoryProtocol


class ListSpeakersUseCase:
    def __init__(self, speaker_repository: SpeakerRepositoryProtocol) -> None:
        self.speaker_repository = speaker_repository

    async def execute(self, params: Params) -> Any:
        return await self.speaker_repository.list_paginated(params)
