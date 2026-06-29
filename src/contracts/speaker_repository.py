from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any, Protocol

from fastapi_pagination import Params

from src.models.speaker import Speaker, SpeakerCreate, SpeakerUpdate


class SpeakerRepositoryProtocol(Protocol):
    def transaction(self) -> AsyncIterator[None]: ...

    async def create(self, data: SpeakerCreate) -> Speaker: ...

    async def get_by_id(self, speaker_id: str) -> Speaker | None: ...

    async def list_by_ids(self, speaker_ids: list[str | int]) -> list[Speaker]: ...

    async def list_paginated(
        self,
        params: Params,
        *,
        name: str | None = None,
        specialty: str | None = None,
        case_sensitive: bool = False,
    ) -> Any: ...

    async def update(self, speaker: Speaker, data: SpeakerUpdate) -> Speaker: ...

    async def delete(self, speaker: Speaker) -> None: ...
