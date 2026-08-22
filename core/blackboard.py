"""Hendelsestavle (blackboard) for MURMUROS-agentene.

Agenter kommuniserer aldri direkte med hverandre: de publiserer hendelser til
tavlen og abonnerer på hendelsestypene de bryr seg om. Det gjør hver agent
utbyttbar og systemet observerbart — hele historikken ligger på tavlen.
"""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Any, Mapping


def _freeze(value: Any) -> Any:
    """Return an immutable copy of supported container values."""
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, set):
        return frozenset(_freeze(item) for item in value)
    return value


def _new_event_id() -> str:
    return uuid.uuid4().hex


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class Event:
    """En uforanderlig hendelse på tavlen.

    'event_type' sier hva som skjedde, 'source' hvem som meldte det, og
    'payload' bærer dataene. Id og tidsstempel settes automatisk.
    """

    event_type: str
    source: str
    payload: Mapping[str, Any]
    event_id: str = field(default_factory=_new_event_id)
    created_at: datetime = field(default_factory=_utcnow)

    def __post_init__(self) -> None:
        if not isinstance(self.event_type, str) or not self.event_type.strip():
            raise ValueError(
                f'event_type must be a non-empty string, got {self.event_type!r}'
            )
        if not isinstance(self.source, str) or not self.source.strip():
            raise ValueError(
                f'source must be a non-empty string, got {self.source!r}'
            )
        if not isinstance(self.payload, dict):
            raise ValueError(
                f'payload must be a dict, got {type(self.payload).__name__}'
            )
        object.__setattr__(self, 'payload', _freeze(self.payload))


class MurmurBlackboard:
    """Enkel asynkron pub/sub-tavle.

    - `subscribe(event_type)` gir en kø som mottar alle fremtidige hendelser
      av den typen (én kø per abonnent — alle abonnenter får alt).
    - `publish(...)` validerer, arkiverer og distribuerer hendelsen.
    - `history` er den komplette, uforanderlige hendelsesloggen.
    """

    def __init__(self) -> None:
        self._subscribers: dict[str, list[asyncio.Queue[Event]]] = {}
        self._history: list[Event] = []

    def subscribe(self, event_type: str) -> asyncio.Queue[Event]:
        """Registrer et abonnement og få inbox-køen for hendelsestypen."""
        if not isinstance(event_type, str) or not event_type.strip():
            raise ValueError(
                f'event_type must be a non-empty string, got {event_type!r}'
            )
        inbox: asyncio.Queue[Event] = asyncio.Queue()
        self._subscribers.setdefault(event_type, []).append(inbox)
        return inbox

    async def publish(
        self, event_type: str, source: str, payload: dict[str, Any]
    ) -> Event:
        """Publiser en hendelse til alle abonnenter. Returnerer hendelsen."""
        event = Event(event_type=event_type, source=source, payload=payload)
        self._history.append(event)
        for inbox in self._subscribers.get(event_type, []):
            await inbox.put(event)
        return event

    @property
    def history(self) -> tuple[Event, ...]:
        """Alle publiserte hendelser i rekkefølge (uforanderlig kopi)."""
        return tuple(self._history)
