import asyncio

import pytest

from core import Event, MurmurBlackboard


def test_event_gets_id_and_timestamp():
    event = Event(event_type='TEST', source='UnitTest', payload={})
    assert event.event_id
    assert event.created_at.tzinfo is not None


def test_event_ids_are_unique():
    a = Event(event_type='TEST', source='UnitTest', payload={})
    b = Event(event_type='TEST', source='UnitTest', payload={})
    assert a.event_id != b.event_id


@pytest.mark.parametrize('bad_kwargs', [
    {'event_type': '', 'source': 'x', 'payload': {}},
    {'event_type': '   ', 'source': 'x', 'payload': {}},
    {'event_type': None, 'source': 'x', 'payload': {}},
    {'event_type': 'TEST', 'source': '', 'payload': {}},
    {'event_type': 'TEST', 'source': 'x', 'payload': 'not-a-dict'},
    {'event_type': 'TEST', 'source': 'x', 'payload': None},
])
def test_event_rejects_invalid_input(bad_kwargs):
    with pytest.raises(ValueError):
        Event(**bad_kwargs)


def test_subscribe_rejects_invalid_event_type():
    bus = MurmurBlackboard()
    with pytest.raises(ValueError):
        bus.subscribe('')


def test_publish_reaches_all_subscribers_and_history():
    async def scenario():
        bus = MurmurBlackboard()
        inbox_a = bus.subscribe('PING')
        inbox_b = bus.subscribe('PING')
        other = bus.subscribe('OTHER')

        published = await bus.publish('PING', 'UnitTest', {'n': 1})

        assert (await inbox_a.get()).event_id == published.event_id
        assert (await inbox_b.get()).event_id == published.event_id
        assert other.empty()
        assert bus.history == (published,)

    asyncio.run(scenario())


def test_publish_without_subscribers_still_archives():
    async def scenario():
        bus = MurmurBlackboard()
        event = await bus.publish('LONELY', 'UnitTest', {})
        assert bus.history == (event,)

    asyncio.run(scenario())


def test_publish_validates_payload():
    async def scenario():
        bus = MurmurBlackboard()
        with pytest.raises(ValueError):
            await bus.publish('BAD', 'UnitTest', 'not-a-dict')
        assert bus.history == ()

    asyncio.run(scenario())


def test_event_payload_is_immutable_and_detached_from_input():
    payload = {'nested': {'items': [1, 2]}}
    event = Event(event_type='TEST', source='UnitTest', payload=payload)

    payload['nested']['items'].append(3)

    assert event.payload['nested']['items'] == (1, 2)
    with pytest.raises(TypeError):
        event.payload['nested']['items'] = ()
