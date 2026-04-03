from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class BaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)