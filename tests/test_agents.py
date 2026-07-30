import asyncio

import agents
from agents import (
    architect_agent,
    growth_and_pedagogue_consolidator,
    observer_agent,
)
from core import MurmurBlackboard


async def _instant_sleep(_seconds):
    return None


def test_full_agent_chain_produces_quest(monkeypatch, capsys):
    """Observer -> Architect -> Pedagogue/Growth ender i en QUEST_GENERATED-
    hendelse med alle tre valg, inkludert Sovereign Override."""
    monkeypatch.setattr(agents.asyncio, 'sleep', _instant_sleep)

    async def scenario():
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
            quest = await asyncio.wait_for(quest_inbox.get(), timeout=5)
        finally:
            for worker in workers:
                worker.cancel()
            await asyncio.gather(*workers, return_exceptions=True)

        return bus, quest

    bus, quest = asyncio.run(scenario())

    assert quest.event_type == 'QUEST_GENERATED'
    assert quest.payload['title'] == 'Protocol: Digital Sundown'
    assert set(quest.payload['options']) == {'A', 'B', 'X'}
    assert quest.payload['xp_rewards'] == {'A': 15, 'B': 5, 'X': 0}

    # Sporbarhet: hele kjeden ligger på tavlen i riktig rekkefølge,
    # og designet peker tilbake på mønsteret som utløste det.
    event_types = [event.event_type for event in bus.history]
    assert event_types == [
        'PATTERN_DETECTED', 'SYSTEM_DESIGN_READY', 'QUEST_GENERATED',
    ]
    pattern, design, _ = bus.history
    assert design.payload['source_event_id'] == pattern.event_id
    assert quest.payload['meta'] is design.payload


def test_workers_cancel_cleanly(monkeypatch):
    """Agenter i while-True-løkke skal dø stille ved kansellering."""
    monkeypatch.setattr(agents.asyncio, 'sleep', _instant_sleep)

    async def scenario():
        bus = MurmurBlackboard()
        worker = asyncio.create_task(
            architect_agent(bus, bus.subscribe('PATTERN_DETECTED'))
        )
        await asyncio.sleep(0)
        worker.cancel()
        results = await asyncio.gather(worker, return_exceptions=True)
        assert isinstance(results[0], asyncio.CancelledError)

    asyncio.run(scenario())
