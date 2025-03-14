from detect_pitch import detect_pitch  # Import the pitch detection function
from pitch_map import get_solfeggio_note  # Import the pitch-to-note mapping function
def detect_vocal_range():
    """
    Detects the user's vocal range by recording and analyzing the notes Do, Re, Mi, etc.
    :return: The user's vocal range.
    """
    solfeggio = ['Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Si']
    notes = []
    
    for syllable in solfeggio:
        pitch = detect_pitch(f"user_{syllable}.wav")  # Record and detect the pitch for each note
        note = get_solfeggio_note(pitch)  # Map the pitch to the corresponding note
        notes.append(note)
        print(f"Note {syllable}: {note}")

    # Identify the vocal range (lowest and highest note)
    print(f"User's vocal range: {min(notes)} to {max(notes)}")

# Run the range detection
detect_vocal_range()
