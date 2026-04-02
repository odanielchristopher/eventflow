from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class EntityModel(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: int | None = None
