"""Animal Signal PsyTech — a dark organic psytrance sketch, 132 BPM, D minor.

Standalone MIDI prototype (same pattern as generate_midi.py) mapping animal
calls onto playable musical roles for the Musikk DNA pipeline stage:

- Wolf howl   -> deep emotional lead, D-F-A-C
- Bird calls  -> delicate rhythmic arpeggios
- Whale song  -> spacious sub-harmonic pad
- Frog sounds -> wet percussive bass stabs
- Raven calls -> sparse transition accents

Instrument `program` numbers are General MIDI placeholders standing in for
sound-designed animal-call patches — swap them for real samples/synths in a
DAW.
"""

from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo

TEMPO_BPM = 132
KEY = 'Dm'
TICKS_PER_BEAT = 480  # quarter note

DEFAULT_FILENAME = 'animal_signal_psytech.mid'

# Each note is a mapping with 'note', 'velocity', 'duration' (ticks the note
# rings for) and optional 'rest' (ticks of silence before the note starts,
# default 0).

WOLF_LEAD_NOTES = [
    {'note': 50, 'velocity': 100, 'duration': 960},  # D3
    {'note': 53, 'velocity': 95, 'duration': 960},   # F3
    {'note': 57, 'velocity': 100, 'duration': 960},  # A3
    {'note': 60, 'velocity': 105, 'duration': 960},  # C4
]

BIRD_ARPEGGIO_NOTES = [
    {'note': 74, 'velocity': 80, 'duration': 240},  # D5
    {'note': 77, 'velocity': 75, 'duration': 240},  # F5
    {'note': 81, 'velocity': 85, 'duration': 240},  # A5
    {'note': 84, 'velocity': 70, 'duration': 240},  # C6
    {'note': 81, 'velocity': 78, 'duration': 240},  # A5
    {'note': 77, 'velocity': 72, 'duration': 240},  # F5
]

WHALE_PAD_NOTES = [
    {'note': 26, 'velocity': 60, 'duration': 3840},  # D1
    {'note': 33, 'velocity': 55, 'duration': 3840},  # A1
]

FROG_BASS_STAB_NOTES = [
    {'note': 38, 'velocity': 110, 'duration': 60},                 # D2
    {'note': 38, 'velocity': 90, 'duration': 60, 'rest': 180},     # D2
    {'note': 41, 'velocity': 105, 'duration': 60, 'rest': 120},    # F2
    {'note': 38, 'velocity': 95, 'duration': 60, 'rest': 240},     # D2
]

RAVEN_TRANSITION_NOTES = [
    {'note': 79, 'velocity': 90, 'duration': 40},                   # G5 caw
    {'note': 79, 'velocity': 70, 'duration': 40, 'rest': 3800},     # G5 caw
]

# (track name, channel, GM program placeholder, notes)
TRACKS = [
    ('Wolf Lead', 0, 61, WOLF_LEAD_NOTES),          # French Horn
    ('Bird Arpeggio', 1, 108, BIRD_ARPEGGIO_NOTES),  # Kalimba
    ('Whale Pad', 2, 89, WHALE_PAD_NOTES),          # Pad 2 (warm)
    ('Frog Bass Stabs', 3, 39, FROG_BASS_STAB_NOTES),  # Synth Bass 2
    ('Raven Transitions', 4, 123, RAVEN_TRANSITION_NOTES),  # Bird Tweet
]


def validate_notes(notes):
    """Validate a sequence of note mappings, raising ValueError on bad input.

    Each note must be a mapping with integer 'note' and 'velocity' in the
    valid MIDI range (0-127), a non-negative integer 'duration' in ticks,
    and an optional non-negative integer 'rest' in ticks. Returns the notes
    unchanged so callers can validate inline.
    """
    for i, n in enumerate(notes):
        try:
            note = n['note']
            velocity = n['velocity']
            duration = n['duration']
            rest = n.get('rest', 0)
        except (TypeError, KeyError, AttributeError):
            raise ValueError(
                f"note {i}: expected a mapping with 'note', 'velocity' and "
                f"'duration' keys, got {n!r}"
            ) from None

        for name, value in (('note', note), ('velocity', velocity)):
            if not isinstance(value, int) or not 0 <= value <= 127:
                raise ValueError(
                    f"note {i}: {name} must be an integer in 0-127, got {value!r}"
                )
        for name, value in (('duration', duration), ('rest', rest)):
            if not isinstance(value, int) or value < 0:
                raise ValueError(
                    f"note {i}: {name} must be a non-negative integer, got {value!r}"
                )
    return notes


def build_track(name, channel, program, notes):
    """Build a named MIDI track on the given channel from a note sequence.

    Each note plays after its 'rest' ticks of silence and is released after
    its 'duration' ticks. Raises ValueError for notes outside valid ranges.
    """
    validate_notes(notes)

    track = MidiTrack()
    track.append(MetaMessage('track_name', name=name, time=0))
    track.append(Message('program_change', channel=channel, program=program, time=0))

    for n in notes:
        rest = n.get('rest', 0)
        track.append(Message(
            'note_on', channel=channel, note=n['note'], velocity=n['velocity'], time=rest,
        ))
        track.append(Message(
            'note_off', channel=channel, note=n['note'], velocity=n['velocity'], time=n['duration'],
        ))

    return track


def build_composition(tracks=None):
    """Build the Animal Signal PsyTech MIDI composition.

    'tracks' defaults to TRACKS: a list of (name, channel, program, notes)
    tuples, one per animal-derived musical role. Returns the constructed
    MidiFile. Raises ValueError for notes outside the valid MIDI ranges.
    """
    if tracks is None:
        tracks = TRACKS

    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)

    conductor = MidiTrack()
    conductor.append(MetaMessage('track_name', name='Animal Signal PsyTech', time=0))
    conductor.append(MetaMessage('set_tempo', tempo=bpm2tempo(TEMPO_BPM), time=0))
    conductor.append(MetaMessage('time_signature', numerator=4, denominator=4, time=0))
    conductor.append(MetaMessage('key_signature', key=KEY, time=0))
    mid.tracks.append(conductor)

    for name, channel, program, notes in tracks:
        mid.tracks.append(build_track(name, channel, program, notes))

    return mid


def save_composition(filename=DEFAULT_FILENAME, tracks=None):
    """Build the composition and save it to 'filename'. Returns the MidiFile."""
    mid = build_composition(tracks)
    mid.save(filename)
    return mid


def main():
    save_composition()
    print(f"MIDI file '{DEFAULT_FILENAME}' created!")


if __name__ == '__main__':
    main()
