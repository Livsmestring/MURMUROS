# core.py
"""Kjernen i Murmur OS: en enkel asynkron «blackboard» (publish/subscribe).

Agenter abonnerer på hendelsestyper (topics) og får en egen innboks-kø. Når
noen publiserer en hendelse, legges den på køen til hver abonnent for den
typen. Dette holder agentene løst koblet — de kjenner bare hendelser, ikke
hverandre.
"""

from __future__ import annotations

import asyncio
import time
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Event:
    """En hendelse på tavla.

    Attributes:
        topic: Hendelsestypen, f.eks. "PATTERN_DETECTED".
        source: Navnet på agenten som publiserte hendelsen.
        payload: Vilkårlige data knyttet til hendelsen.
        event_id: Unik id, generert automatisk.
        timestamp: Unix-tid da hendelsen ble opprettet.
    """

    topic: str
    source: str
    payload: dict[str, Any]
    event_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    timestamp: float = field(default_factory=time.time)


class MurmurBlackboard:
    """En minimal asynkron publish/subscribe-tavle.

    Abonnenter kaller :meth:`subscribe` for å få en kø for en hendelsestype.
    :meth:`publish` legger en ny :class:`Event` på køen til hver abonnent for
    den typen, og tar vare på en historikk over alt som er publisert.
    """

    def __init__(self) -> None:
        self._subscribers: dict[str, list[asyncio.Queue[Event]]] = {}
        self.history: list[Event] = []

    def subscribe(self, topic: str) -> asyncio.Queue[Event]:
        """Abonner på en hendelsestype og få en egen innboks-kø tilbake."""
        queue: asyncio.Queue[Event] = asyncio.Queue()
        self._subscribers.setdefault(topic, []).append(queue)
        return queue

    async def publish(self, topic: str, source: str, payload: dict[str, Any]) -> Event:
        """Publiser en hendelse til alle abonnenter for ``topic``.

        Returnerer den opprettede :class:`Event`-en.
        """
        event = Event(topic=topic, source=source, payload=payload)
        self.history.append(event)
        for queue in self._subscribers.get(topic, []):
            await queue.put(event)
        return event
