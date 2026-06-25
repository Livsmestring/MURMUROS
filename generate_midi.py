from mido import Message, MidiFile, MidiTrack

# Define notes for the bassline
NOTES = [
    {'note': 45, 'velocity': 70, 'duration': 480},  # A2
    {'note': 48, 'velocity': 70, 'duration': 480},  # C3
    {'note': 50, 'velocity': 70, 'duration': 480},  # D3
    {'note': 52, 'velocity': 70, 'duration': 480},  # E3
]

DEFAULT_FILENAME = 'bassline.mid'


def build_bassline(notes=NOTES):
    """Build a MidiFile containing a single track with the given bassline notes.

    Each note produces a ``note_on`` immediately followed by a ``note_off``
    after ``duration`` ticks. Returns the constructed ``MidiFile``.
    """
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    for n in notes:
        track.append(Message('note_on', note=n['note'], velocity=n['velocity'], time=0))
        track.append(Message('note_off', note=n['note'], velocity=n['velocity'], time=n['duration']))

    return mid


def main(filename=DEFAULT_FILENAME):
    """Build the bassline and save it to ``filename``."""
    mid = build_bassline()
    mid.save(filename)
    print(f"MIDI file '{filename}' created!")
    return filename


if __name__ == '__main__':
    main()
