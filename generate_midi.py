from mido import Message, MidiFile, MidiTrack

# Define notes for the bassline
NOTES = [
    {'note': 45, 'velocity': 70, 'duration': 480},  # A2
    {'note': 48, 'velocity': 70, 'duration': 480},  # C3
    {'note': 50, 'velocity': 70, 'duration': 480},  # D3
    {'note': 52, 'velocity': 70, 'duration': 480},  # E3
]


def build_bassline_track(notes):
    track = MidiTrack()
    for n in notes:
        track.append(Message('note_on', note=n['note'], velocity=n['velocity'], time=0))
        track.append(Message('note_off', note=n['note'], velocity=n['velocity'], time=n['duration']))
    return track


def build_bassline_midi(notes=NOTES):
    mid = MidiFile()
    mid.tracks.append(build_bassline_track(notes))
    return mid


def main():
    mid = build_bassline_midi()
    mid.save('bassline.mid')
    print("MIDI file 'bassline.mid' created!")


if __name__ == '__main__':
    main()
