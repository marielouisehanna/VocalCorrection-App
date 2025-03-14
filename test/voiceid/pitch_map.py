# Mapping pitch (frequency) to solfège syllables
note_frequencies = {
    'Do': 261.63,  # C4
    'Re': 293.66,  # D4
    'Mi': 329.63,  # E4
    'Fa': 349.23,  # F4
    'Sol': 392.00, # G4
    'La': 440.00,  # A4
    'Si': 493.88   # B4
}

def get_solfeggio_note(pitch):
    """
    Maps a detected pitch (in Hz) to the closest solfège syllable.
    :param pitch: The detected pitch in Hz.
    :return: The solfège syllable corresponding to the pitch.
    """
    # Find the closest solfège note based on the detected pitch
    closest_note = min(note_frequencies, key=lambda x: abs(note_frequencies[x] - pitch))
    return closest_note

# Test the mapping
pitch = 440  # Hz, A4
note = get_solfeggio_note(pitch)
print(f"The detected pitch corresponds to the note: {note}")
