# agents.py
from __future__ import annotations

import asyncio

from core import Event, MurmurBlackboard


async def observer_agent(bus: MurmurBlackboard) -> None:
    """Speider etter mønstre i hverdagen (her simulert med et søvn-eksempel)."""
    print("👀 [Observer] Sjekker logger, vaner og input...")
    await asyncio.sleep(1)

    payload = {
        "pattern_name": "Natt-skrolling og redusert søvnkvalitet",
        "raw_data": "Brukeren har registrert aktivitet på telefonen frem til kl. 01:30 tre dager på rad.",
        "impact": "Redusert fokus på Murmur OS-arkitektur dagen etter.",
    }
    await bus.publish("PATTERN_DETECTED", "ObserverAgent", payload)


async def architect_agent(bus: MurmurBlackboard, inbox: asyncio.Queue[Event]) -> None:
    """Tar mønsteret og designer et robust livs-system."""
    while True:
        event = await inbox.get()
        try:
            print("\n🧠 [Architect] Mønster mottatt. Tegner opp et nytt livs-system...")
            await asyncio.sleep(1.5)

            payload = {
                "system_name": "The Digital Sundown Protocol",
                "blueprint": (
                    "Automatisk nedstenging av underholdningsapper kl 22:30. "
                    "Aktivere omgivelseslyd (Dark Techno/Cinematic) for overgang."
                ),
                "source_event_id": event.event_id,
            }
            await bus.publish("SYSTEM_DESIGN_READY", "ArchitectAgent", payload)
        finally:
            inbox.task_done()


async def growth_and_pedagogue_consolidator(
    bus: MurmurBlackboard, inbox: asyncio.Queue[Event]
) -> None:
    """Gjør systemet skalerbart og oversetter det til spill-opsjoner."""
    while True:
        event = await inbox.get()
        try:
            print("🎓 [Pedagogue] Bryter ned kompleksiteten...")
            print("📈 [Growth] Beregner gevinster for livskvalitet og fokus...")
            await asyncio.sleep(1.5)

            quest_payload = {
                "title": "Protocol: Digital Sundown",
                "options": {
                    "A": "Iverksett protokollen fullt ut (Gain: +15 XP, +10% Fokus i morgen).",
                    "B": "Modifiser protokollen: Skyv tiden til 23:30 (Gain: +5 XP).",
                    "X": "Avvis (Sovereign Override: Jeg styrer dette selv).",
                },
                "xp_rewards": {"A": 15, "B": 5, "X": 0},
                "meta": event.payload,
            }
            await bus.publish("QUEST_GENERATED", "CoreTeam", quest_payload)
        finally:
            inbox.task_done()
