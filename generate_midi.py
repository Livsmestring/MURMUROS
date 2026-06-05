from mido import Message, MidiFile, MidiTrack

# Create a new MIDI file and track
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Define notes for the bassline
notes = [
    {'note': 45, 'velocity': 70, 'duration': 480},  # A2
    {'note': 48, 'velocity': 70, 'duration': 480},  # C3
    {'note': 50, 'velocity': 70, 'duration': 480},  # D3
    {'note': 52, 'velocity': 70, 'duration': 480},  # E3
]

# Add notes to the track
for n in notes:
    track.append(Message('note_on', note=n['note'], velocity=n['velocity'], time=0))
    track.append(Message('note_off', note=n['note'], velocity=n['velocity'], time=n['duration']))

# Save the MIDI file
mid.save('bassline.mid')
print("MIDI file 'bassline.mid' created!")