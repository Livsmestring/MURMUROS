import asyncio

import pytest

import demo
from core import MurmurBlackboard


class TrackingBlackboard(MurmurBlackboard):
    """Expose the demo-created bus so the test can verify the full history."""

    latest = None

    def __init__(self):
        super().__init__()
        type(self).latest = self


def install_task_tracker(monkeypatch):
    created_tasks = []
    original_create_task = asyncio.create_task

    def create_task(coro, *args, **kwargs):
        task = original_create_task(coro, *args, **kwargs)
        created_tasks.append(task)
        return task

    monkeypatch.setattr(asyncio, 'create_task', create_task)
    return created_tasks


def test_run_pipeline_covers_observer_to_quest(monkeypatch, capsys):
    async def scenario():
        monkeypatch.setattr(demo, 'MurmurBlackboard', TrackingBlackboard)
        monkeypatch.setattr(demo.asyncio, 'sleep', lambda _seconds: _completed())
        await demo.run_pipeline()

    asyncio.run(scenario())

    output = capsys.readouterr().out
    history = TrackingBlackboard.latest.history

    assert [event.event_type for event in history] == [
        'PATTERN_DETECTED',
        'SYSTEM_DESIGN_READY',
        'QUEST_GENERATED',
    ]
    assert history[1].payload['source_event_id'] == history[0].event_id
    assert history[2].payload['meta'] == history[1].payload
    assert history[2].payload['meta']['source_event_id'] == history[0].event_id
    assert history[2].payload['options']['X'].startswith('Avvis')
    assert 'QUEST: Protocol: Digital Sundown' in output
    assert '[A]' in output
    assert '[B]' in output
    assert '[X]' in output
    assert 'Hendelser på tavlen: 3' in output


def test_run_pipeline_cancels_workers_when_quest_times_out(monkeypatch):
    async def scenario():
        created_tasks = install_task_tracker(monkeypatch)
        monkeypatch.setattr(demo, 'observer_agent', _no_op_observer)
        monkeypatch.setattr(demo, 'QUEST_TIMEOUT_SECONDS', 0.01)

        with pytest.raises(asyncio.TimeoutError):
            await demo.run_pipeline()

        assert len(created_tasks) == 2
        assert all(task.done() and task.cancelled() for task in created_tasks)

    asyncio.run(scenario())


async def _completed():
    return None


async def _no_op_observer(_bus):
    return None
