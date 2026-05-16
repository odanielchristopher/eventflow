from src.routes.document import router as document_router
from src.routes.event import router as event_router
from src.routes.hash import router as hash_router
from src.routes.speaker import router as speaker_router
from src.routes.subscription import router as subscription_router

__all__ = [
    "document_router",
    "event_router",
    "hash_router",
    "speaker_router",
    "subscription_router",
]
