from mido import Message, MidiFile, MidiTrack

# Default notes for the bassline (note, velocity, duration in ticks)
DEFAULT_NOTES = [
    {'note': 45, 'velocity': 70, 'duration': 480},  # A2
    {'note': 48, 'velocity': 70, 'duration': 480},  # C3
    {'note': 50, 'velocity': 70, 'duration': 480},  # D3
    {'note': 52, 'velocity': 70, 'duration': 480},  # E3
]

DEFAULT_FILENAME = 'bassline.mid'


def validate_notes(notes):
    """Validate a sequence of note mappings, raising ValueError on bad input.

    Each note must be a mapping with integer 'note' and 'velocity' in the
    valid MIDI range (0-127) and a non-negative integer 'duration' in ticks.
    Returns the notes unchanged so callers can validate inline.
    """
    for i, n in enumerate(notes):
        try:
            note = n['note']
            velocity = n['velocity']
            duration = n['duration']
        except (TypeError, KeyError):
            raise ValueError(
                f"note {i}: expected a mapping with 'note', 'velocity' and "
                f"'duration' keys, got {n!r}"
            ) from None

        for name, value in (('note', note), ('velocity', velocity)):
            if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 127:
                raise ValueError(
                    f"note {i}: {name} must be an integer in 0-127, got {value!r}"
                )
        if isinstance(duration, bool) or not isinstance(duration, int) or duration < 0:
            raise ValueError(
                f"note {i}: duration must be a non-negative integer, got {duration!r}"
            )
    return notes


def build_bassline(notes=None):
    """Build a MIDI file containing a bassline from the given notes.

    Each note is a mapping with 'note', 'velocity' and 'duration' keys.
    The note plays immediately (note_on at time 0) and is released after
    'duration' ticks (note_off). Returns the constructed MidiFile.
    Raises ValueError for notes outside the valid MIDI ranges.
    """
    if notes is None:
        notes = DEFAULT_NOTES
    validate_notes(notes)

    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    for n in notes:
        track.append(Message('note_on', note=n['note'], velocity=n['velocity'], time=0))
        track.append(Message('note_off', note=n['note'], velocity=n['velocity'], time=n['duration']))

    return mid


def save_bassline(filename=DEFAULT_FILENAME, notes=None):
    """Build the bassline and save it to 'filename'. Returns the MidiFile."""
    mid = build_bassline(notes)
    mid.save(filename)
    return mid


def main():
    save_bassline()
    print(f"MIDI file '{DEFAULT_FILENAME}' created!")


if __name__ == '__main__':
    main()
