from __future__ import annotations

from src.models.base import BaseModel
from src.models.hash.hash_algorithm import HashAlgorithm

class CreateHashDto(BaseModel):
    text: str
    algorithm: HashAlgorithm
