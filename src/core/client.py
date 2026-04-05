from __future__ import annotations

from pathlib import Path

from src.core.repository import DeltaLakeRepository
from src.models import Activity, CheckIn, Event, Subscription, Speaker


class DeltaLakeClient:
    def __init__(self, base_path: str | Path = "src/data") -> None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

        self.subscriptions = DeltaLakeRepository(self.base_path, "subscriptions", Subscription)
        self.events = DeltaLakeRepository(self.base_path, "events", Event)
        self.speakers = DeltaLakeRepository(self.base_path, "speakers", Speaker)
        self.activities = DeltaLakeRepository(self.base_path, "activities", Activity)
        self.checkins = DeltaLakeRepository(self.base_path, "checkins", CheckIn)

        self.event = self.events

delta_lake_cli = DeltaLakeClient()
