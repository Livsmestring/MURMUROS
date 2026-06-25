from mido import Message, MidiFile, MidiTrack

# Default notes for the bassline (note, velocity, duration in ticks)
DEFAULT_NOTES = [
    {'note': 45, 'velocity': 70, 'duration': 480},  # A2
    {'note': 48, 'velocity': 70, 'duration': 480},  # C3
    {'note': 50, 'velocity': 70, 'duration': 480},  # D3
    {'note': 52, 'velocity': 70, 'duration': 480},  # E3
]

DEFAULT_FILENAME = 'bassline.mid'


def build_bassline(notes=None):
    """Build a MIDI file containing a bassline from the given notes.

    Each note is a mapping with 'note', 'velocity' and 'duration' keys.
    The note plays immediately (note_on at time 0) and is released after
    'duration' ticks (note_off). Returns the constructed MidiFile.
    """
    if notes is None:
        notes = DEFAULT_NOTES

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
