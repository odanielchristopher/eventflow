from __future__ import annotations

from collections import defaultdict

from src.models.document import Document, DocumentRead
from src.models.event import EventEntity, EventRead


def serialize_document(document: Document) -> DocumentRead:
    payload = document.model_dump(exclude={"id"}, mode="python")
    payload["id"] = str(document.id)
    payload["event_id"] = document.event_id
    return DocumentRead.model_validate(payload)


def serialize_event(event: EventEntity, documents: list[Document]) -> EventRead:
    payload = event.model_dump(exclude={"id"}, mode="python")
    payload["id"] = str(event.id)
    payload["documents"] = [
        serialize_document(document).model_dump(mode="python")
        for document in documents
    ]
    return EventRead.model_validate(payload)


def group_documents_by_event_id(documents: list[Document]) -> dict[str, list[Document]]:
    grouped: dict[str, list[Document]] = defaultdict(list)
    for document in documents:
        if document.event_id is not None:
            grouped[document.event_id].append(document)
    return grouped
