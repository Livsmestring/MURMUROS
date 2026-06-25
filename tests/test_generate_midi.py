import os

import pytest
from mido import MidiFile

import generate_midi


def test_notes_are_valid_midi_values():
    """Every note and velocity must be within the valid MIDI range (0-127)
    and durations must be non-negative."""
    for n in generate_midi.NOTES:
        assert 0 <= n['note'] <= 127
        assert 0 <= n['velocity'] <= 127
        assert n['duration'] >= 0


def test_build_bassline_has_single_track():
    mid = generate_midi.build_bassline()
    assert len(mid.tracks) == 1


def test_build_bassline_emits_note_on_off_pairs():
    """Each input note should produce one note_on and one note_off message."""
    mid = generate_midi.build_bassline()
    messages = [msg for msg in mid.tracks[0] if msg.type in ('note_on', 'note_off')]

    assert len(messages) == 2 * len(generate_midi.NOTES)

    for i, n in enumerate(generate_midi.NOTES):
        note_on = messages[2 * i]
        note_off = messages[2 * i + 1]

        assert note_on.type == 'note_on'
        assert note_on.note == n['note']
        assert note_on.velocity == n['velocity']
        assert note_on.time == 0

        assert note_off.type == 'note_off'
        assert note_off.note == n['note']
        assert note_off.time == n['duration']


def test_build_bassline_respects_custom_notes():
    custom = [{'note': 60, 'velocity': 64, 'duration': 240}]
    mid = generate_midi.build_bassline(custom)
    messages = [msg for msg in mid.tracks[0] if msg.type in ('note_on', 'note_off')]
    assert len(messages) == 2
    assert messages[0].note == 60
    assert messages[1].time == 240


def test_main_writes_a_readable_file(tmp_path):
    """The saved file must exist and round-trip back through mido."""
    target = tmp_path / 'out.mid'
    returned = generate_midi.main(str(target))

    assert returned == str(target)
    assert os.path.exists(target)

    reloaded = MidiFile(str(target))
    messages = [msg for msg in reloaded.tracks[0] if msg.type in ('note_on', 'note_off')]
    assert len(messages) == 2 * len(generate_midi.NOTES)
