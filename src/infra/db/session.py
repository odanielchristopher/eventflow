from __future__ import annotations

from collections.abc import AsyncGenerator

async def get_async_session() -> AsyncGenerator[None, None]:
    yield None
