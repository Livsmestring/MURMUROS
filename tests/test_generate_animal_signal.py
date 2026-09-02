import os

import pytest
from mido import MidiFile, bpm2tempo

import generate_animal_signal as ras


ALL_NOTE_SEQUENCES = [
    ras.WOLF_LEAD_NOTES,
    ras.BIRD_ARPEGGIO_NOTES,
    ras.WHALE_PAD_NOTES,
    ras.FROG_BASS_STAB_NOTES,
    ras.RAVEN_TRANSITION_NOTES,
]


@pytest.mark.parametrize('notes', ALL_NOTE_SEQUENCES)
def test_default_note_sequences_are_valid_midi_values(notes):
    for n in notes:
        assert 0 <= n['note'] <= 127
        assert 0 <= n['velocity'] <= 127
        assert n['duration'] >= 0
        assert n.get('rest', 0) >= 0


def test_tracks_reference_known_note_sequences():
    names = [name for name, _channel, _program, _notes in ras.TRACKS]
    assert names == [
        'Wolf Lead',
        'Bird Arpeggio',
        'Whale Pad',
        'Frog Bass Stabs',
        'Raven Transitions',
    ]


def test_build_track_message_count():
    # track_name + program_change + a note_on/note_off pair per note.
    track = ras.build_track('Wolf Lead', 0, 61, ras.WOLF_LEAD_NOTES)
    assert len(track) == 2 + 2 * len(ras.WOLF_LEAD_NOTES)


def test_build_track_note_on_off_and_rest():
    notes = [
        {'note': 38, 'velocity': 110, 'duration': 60},
        {'note': 41, 'velocity': 90, 'duration': 60, 'rest': 180},
    ]
    track = ras.build_track('Frog Bass Stabs', 3, 39, notes)

    # track_name, program_change, then note_on/note_off pairs.
    assert track[0].type == 'track_name'
    program_change = track[1]
    assert program_change.type == 'program_change'
    assert program_change.channel == 3
    assert program_change.program == 39

    first_on, first_off, second_on, second_off = track[2:]

    assert first_on.type == 'note_on'
    assert first_on.channel == 3
    assert first_on.note == 38
    assert first_on.time == 0  # no 'rest' key => defaults to 0
    assert first_off.type == 'note_off'
    assert first_off.time == 60

    assert second_on.type == 'note_on'
    assert second_on.note == 41
    assert second_on.time == 180  # explicit rest before the stab
    assert second_off.time == 60


@pytest.mark.parametrize('bad_note', [
    {'note': 128, 'velocity': 70, 'duration': 480},   # note above MIDI range
    {'note': -1, 'velocity': 70, 'duration': 480},    # note below MIDI range
    {'note': 60, 'velocity': 200, 'duration': 480},   # velocity above range
    {'note': 60, 'velocity': 70, 'duration': -1},     # negative duration
    {'note': 60, 'velocity': 70, 'duration': 480, 'rest': -1},  # negative rest
    {'note': 'D3', 'velocity': 70, 'duration': 480},  # wrong type
    {'velocity': 70, 'duration': 480},                # missing 'note' key
    'not-a-mapping',                                  # not a mapping at all
])
def test_build_track_rejects_invalid_notes(bad_note):
    with pytest.raises(ValueError):
        ras.build_track('Test', 0, 0, [bad_note])


def test_validate_notes_returns_input_unchanged():
    notes = [{'note': 60, 'velocity': 64, 'duration': 120}]
    assert ras.validate_notes(notes) is notes


def test_build_composition_track_count():
    mid = ras.build_composition()
    assert len(mid.tracks) == 1 + len(ras.TRACKS)  # conductor + one per role


def test_build_composition_ticks_per_beat():
    mid = ras.build_composition()
    assert mid.ticks_per_beat == ras.TICKS_PER_BEAT


def test_build_composition_conductor_meta():
    mid = ras.build_composition()
    conductor = mid.tracks[0]

    tempo_msg = next(m for m in conductor if m.type == 'set_tempo')
    assert tempo_msg.tempo == bpm2tempo(ras.TEMPO_BPM)

    time_sig = next(m for m in conductor if m.type == 'time_signature')
    assert (time_sig.numerator, time_sig.denominator) == (4, 4)

    key_sig = next(m for m in conductor if m.type == 'key_signature')
    assert key_sig.key == ras.KEY


def test_build_composition_does_not_write_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    ras.build_composition()
    assert os.listdir(tmp_path) == []


def test_save_composition_writes_readable_file(tmp_path):
    target = tmp_path / 'out.mid'
    ras.save_composition(str(target))

    assert target.exists()

    reloaded = MidiFile(str(target))
    assert len(reloaded.tracks) == 1 + len(ras.TRACKS)


def test_save_composition_default_filename(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    ras.save_composition()
    assert (tmp_path / ras.DEFAULT_FILENAME).exists()


def test_main_creates_file_and_prints(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    ras.main()

    out = capsys.readouterr().out
    assert ras.DEFAULT_FILENAME in out
    assert (tmp_path / ras.DEFAULT_FILENAME).exists()
