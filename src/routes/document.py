from __future__ import annotations

from fastapi import APIRouter, Depends, File, Response, UploadFile, status
from fastapi_pagination import Page, Params
from fastapi.responses import FileResponse

from src.dependencies.usecases import (
    get_create_document_usecase,
    get_delete_document_usecase,
    get_document_by_id_usecase,
    get_download_document_usecase,
    get_list_event_documents_usecase,
    get_replace_document_usecase,
)
from src.models.document import DocumentRead
from src.usecases.document import (
    CreateDocumentUseCase,
    DeleteDocumentUseCase,
    DownloadDocumentUseCase,
    GetDocumentByIdUseCase,
    ListEventDocumentsUseCase,
    ReplaceDocumentUseCase,
)


router = APIRouter(tags=["documents"])


@router.post(
    "/events/{event_id}/documents",
    response_model=DocumentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_document_for_event(
    event_id: int,
    file: UploadFile = File(...),
    usecase: CreateDocumentUseCase = Depends(get_create_document_usecase),
):
    return await usecase.execute(event_id, file)


@router.get("/events/{event_id}/documents", response_model=Page[DocumentRead])
async def list_event_documents(
    event_id: int,
    params: Params = Depends(),
    usecase: ListEventDocumentsUseCase = Depends(get_list_event_documents_usecase),
):
    return await usecase.execute(event_id, params)


@router.get("/documents/{document_id}", response_model=DocumentRead)
async def get_document_by_id(
    document_id: int,
    usecase: GetDocumentByIdUseCase = Depends(get_document_by_id_usecase),
):
    return await usecase.execute(document_id)


@router.get("/documents/{document_id}/download", response_class=FileResponse)
async def download_document(
    document_id: int,
    usecase: DownloadDocumentUseCase = Depends(get_download_document_usecase),
):
    return await usecase.execute(document_id)


@router.put("/documents/{document_id}", response_model=DocumentRead)
async def replace_document(
    document_id: int,
    file: UploadFile = File(...),
    usecase: ReplaceDocumentUseCase = Depends(get_replace_document_usecase),
):
    return await usecase.execute(document_id, file)


@router.delete(
    "/documents/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def delete_document(
    document_id: int,
    usecase: DeleteDocumentUseCase = Depends(get_delete_document_usecase),
) -> Response:
    await usecase.execute(document_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
