from __future__ import annotations

from collections import defaultdict

from src.models.activity import Activity, ActivityRead
from src.models.speaker import Speaker, SpeakerRead


def serialize_speaker(speaker: Speaker) -> SpeakerRead:
    payload = speaker.model_dump(exclude={"id"}, mode="python")
    payload["id"] = str(speaker.id)
    return SpeakerRead.model_validate(payload)


def serialize_activity(activity: Activity, speakers: list[Speaker]) -> ActivityRead:
    payload = activity.model_dump(exclude={"id"}, mode="python")
    payload["id"] = str(activity.id)
    payload["event_id"] = activity.event_id
    payload["speaker_ids"] = activity.speaker_ids
    payload["speakers"] = [serialize_speaker(speaker).model_dump(mode="python") for speaker in speakers]
    return ActivityRead.model_validate(payload)


def group_speakers_by_id(speakers: list[Speaker]) -> dict[str, Speaker]:
    return {str(speaker.id): speaker for speaker in speakers}


def collect_speaker_ids(activities: list[Activity]) -> list[str]:
    ordered_ids: list[str] = []
    seen: set[str] = set()
    for activity in activities:
        for speaker_id in activity.speaker_ids:
            if speaker_id not in seen:
                seen.add(speaker_id)
                ordered_ids.append(speaker_id)
    return ordered_ids
