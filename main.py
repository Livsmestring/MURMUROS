# main.py
"""Kjørbar demo av Murmur OS-agentflyten.

Kobler agentene på tavla og kjører hele kjeden én gang:

    Observer  --PATTERN_DETECTED-->  Architect
              --SYSTEM_DESIGN_READY-->  Pedagogue/Growth
              --QUEST_GENERATED-->  (vises til brukeren)

Kjør med:  python main.py
"""

from __future__ import annotations

import asyncio

from agents import (
    architect_agent,
    growth_and_pedagogue_consolidator,
    observer_agent,
)
from core import MurmurBlackboard


async def run_pipeline() -> dict:
    """Kjør agentkjeden én gang og returner det genererte oppdraget (quest)."""
    bus = MurmurBlackboard()

    # Hver agent abonnerer på hendelsestypen den reagerer på.
    architect_inbox = bus.subscribe("PATTERN_DETECTED")
    consolidator_inbox = bus.subscribe("SYSTEM_DESIGN_READY")
    quest_inbox = bus.subscribe("QUEST_GENERATED")

    # De to «arbeider»-agentene kjører i uendelige løkker, så vi starter dem
    # som bakgrunnsoppgaver og avslutter dem når oppdraget er klart.
    workers = [
        asyncio.create_task(architect_agent(bus, architect_inbox)),
        asyncio.create_task(
            growth_and_pedagogue_consolidator(bus, consolidator_inbox)
        ),
    ]

    try:
        # Observer setter kjeden i gang.
        await observer_agent(bus)
        # Vent på det ferdige oppdraget lengst nede i kjeden.
        quest_event = await quest_inbox.get()
    finally:
        for worker in workers:
            worker.cancel()
        await asyncio.gather(*workers, return_exceptions=True)

    return quest_event.payload


def render_quest(quest: dict) -> None:
    """Skriv oppdraget pent til terminalen."""
    print("\n" + "=" * 48)
    print(f"🎮 QUEST: {quest['title']}")
    print("=" * 48)
    for key, description in quest["options"].items():
        print(f"  [{key}] {description}")
    print("=" * 48)


async def main() -> None:
    quest = await run_pipeline()
    render_quest(quest)


if __name__ == "__main__":
    asyncio.run(main())
