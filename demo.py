"""Kjørbar demo av MURMUROS-agentkjeden.

    python demo.py

Observer oppdager et mønster, Architect designer et livs-system, og
Pedagogue/Growth leverer en quest brukeren kan velge fra. Demoen venter
på quest-hendelsen (med tidsavbrudd) og stenger agentene rent etterpå.
"""

from __future__ import annotations

import asyncio

from agents import (
    architect_agent,
    growth_and_pedagogue_consolidator,
    observer_agent,
)
from core import MurmurBlackboard

QUEST_TIMEOUT_SECONDS = 10


async def run_pipeline() -> None:
    bus = MurmurBlackboard()

    architect_inbox = bus.subscribe('PATTERN_DETECTED')
    consolidator_inbox = bus.subscribe('SYSTEM_DESIGN_READY')
    quest_inbox = bus.subscribe('QUEST_GENERATED')

    workers = [
        asyncio.create_task(architect_agent(bus, architect_inbox)),
        asyncio.create_task(
            growth_and_pedagogue_consolidator(bus, consolidator_inbox)
        ),
    ]

    try:
        await observer_agent(bus)
        quest = await asyncio.wait_for(
            quest_inbox.get(), timeout=QUEST_TIMEOUT_SECONDS
        )

        print(f"\n⚔️  QUEST: {quest.payload['title']}")
        for key, text in quest.payload['options'].items():
            print(f'   [{key}] {text}')
        print(f'\n📜 Hendelser på tavlen: {len(bus.history)}')
    except TimeoutError:
        print(
            f'\n⏱️  Ingen quest innen {QUEST_TIMEOUT_SECONDS}s — '
            'en agent svarte ikke. Avbryter rent.'
        )
    finally:
        for worker in workers:
            worker.cancel()
        await asyncio.gather(*workers, return_exceptions=True)


def main() -> None:
    asyncio.run(run_pipeline())


if __name__ == '__main__':
    main()
