from generate_midi import NOTES, build_bassline_midi, build_bassline_track


def test_build_bassline_track_emits_note_on_off_pairs_in_order():
    notes = [{'note': 60, 'velocity': 100, 'duration': 240}]
    track = build_bassline_track(notes)

    assert [msg.type for msg in track] == ['note_on', 'note_off']
    note_on, note_off = track
    assert note_on.note == 60 and note_on.velocity == 100 and note_on.time == 0
    assert note_off.note == 60 and note_off.velocity == 100 and note_off.time == 240


def test_build_bassline_track_handles_multiple_notes():
    notes = [
        {'note': 45, 'velocity': 70, 'duration': 480},
        {'note': 48, 'velocity': 80, 'duration': 240},
    ]
    track = build_bassline_track(notes)

    assert len(track) == 4
    assert [msg.note for msg in track] == [45, 45, 48, 48]
    assert [msg.type for msg in track] == ['note_on', 'note_off', 'note_on', 'note_off']


def test_build_bassline_midi_contains_one_track_with_default_notes():
    mid = build_bassline_midi()

    assert len(mid.tracks) == 1
    assert len(mid.tracks[0]) == len(NOTES) * 2


def test_build_bassline_midi_is_saveable_and_loadable(tmp_path):
    mid = build_bassline_midi()
    out_file = tmp_path / 'bassline.mid'

    mid.save(str(out_file))

    assert out_file.exists()
    from mido import MidiFile
    reloaded = MidiFile(str(out_file))
    assert len(reloaded.tracks) == 1
