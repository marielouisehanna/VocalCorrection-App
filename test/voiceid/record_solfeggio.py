import sounddevice as sd
import soundfile as sf

# Function to record a note
def record_note(syllable, filename, duration=3, samplerate=44100):
    """
    Records the user's singing of a note for a given duration.
    :param syllable: The solfège syllable (Do, Re, Mi, etc.)
    :param filename: The filename where the audio will be saved.
    :param duration: The duration of the recording in seconds.
    :param samplerate: The sample rate of the audio.
    """
    print(f"Recording {syllable}... Sing the note now!")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is done
    sf.write(filename, audio_data, samplerate)  # Save the audio to file
    print(f"Recording saved as {filename}")

# Record the solfège syllables
solfeggio = ['Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Si']
for syllable in solfeggio:
    record_note(syllable, f"user_{syllable}.wav")  # Save as user_Do.wav, user_Re.wav, etc.