import os

from mido import MidiFile

import generate_midi


def test_default_notes_are_valid_midi_values():
    # Every note and velocity must be within the valid MIDI range (0-127)
    # and durations must be non-negative.
    for note in generate_midi.DEFAULT_NOTES:
        assert 0 <= note['note'] <= 127
        assert 0 <= note['velocity'] <= 127
        assert note['duration'] >= 0


def test_build_bassline_default_track_count():
    mid = generate_midi.build_bassline()
    assert len(mid.tracks) == 1


def test_build_bassline_message_count():
    # Each note produces a note_on and a note_off message.
    mid = generate_midi.build_bassline()
    track = mid.tracks[0]
    assert len(track) == 2 * len(generate_midi.DEFAULT_NOTES)


def test_build_bassline_note_on_off_pairs():
    mid = generate_midi.build_bassline()
    track = mid.tracks[0]

    for i, note in enumerate(generate_midi.DEFAULT_NOTES):
        note_on = track[2 * i]
        note_off = track[2 * i + 1]

        assert note_on.type == 'note_on'
        assert note_on.note == note['note']
        assert note_on.velocity == note['velocity']
        assert note_on.time == 0

        assert note_off.type == 'note_off'
        assert note_off.note == note['note']
        assert note_off.velocity == note['velocity']
        assert note_off.time == note['duration']


def test_build_bassline_default_notes_match_spec():
    # Guards the documented A2/C3/D3/E3 bassline (note, velocity, duration).
    assert generate_midi.DEFAULT_NOTES == [
        {'note': 45, 'velocity': 70, 'duration': 480},
        {'note': 48, 'velocity': 70, 'duration': 480},
        {'note': 50, 'velocity': 70, 'duration': 480},
        {'note': 52, 'velocity': 70, 'duration': 480},
    ]


def test_build_bassline_custom_notes():
    notes = [{'note': 60, 'velocity': 100, 'duration': 240}]
    mid = generate_midi.build_bassline(notes)
    track = mid.tracks[0]

    assert len(track) == 2
    assert track[0].note == 60
    assert track[0].velocity == 100
    assert track[1].time == 240


def test_build_bassline_empty_notes():
    mid = generate_midi.build_bassline([])
    assert len(mid.tracks) == 1
    assert len(mid.tracks[0]) == 0


def test_build_bassline_does_not_write_file(tmp_path, monkeypatch):
    # Building must be side-effect free: no file should be created.
    monkeypatch.chdir(tmp_path)
    generate_midi.build_bassline()
    assert os.listdir(tmp_path) == []


def test_save_bassline_writes_readable_file(tmp_path):
    target = tmp_path / 'out.mid'
    generate_midi.save_bassline(str(target))

    assert target.exists()

    # The written file should be a valid MIDI file that round-trips.
    reloaded = MidiFile(str(target))
    assert len(reloaded.tracks) == 1
    assert len(reloaded.tracks[0]) >= 2 * len(generate_midi.DEFAULT_NOTES)


def test_save_bassline_default_filename(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    generate_midi.save_bassline()
    assert (tmp_path / generate_midi.DEFAULT_FILENAME).exists()


def test_main_creates_file_and_prints(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    generate_midi.main()

    out = capsys.readouterr().out
    assert generate_midi.DEFAULT_FILENAME in out
    assert (tmp_path / generate_midi.DEFAULT_FILENAME).exists()
