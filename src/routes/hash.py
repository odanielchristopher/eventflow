from __future__ import annotations

from fastapi import APIRouter

from src.models.hash import CreateHashDto

from src.usecases.hash import CreateHashUseCase


router = APIRouter(prefix="/hashes", tags=["hashes"])

@router.post('')
def apply_hash(dto: CreateHashDto):
    return CreateHashUseCase().execute(dto)
