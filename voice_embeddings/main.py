import os
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
from resemblyzer import VoiceEncoder
import numpy as np
import librosa

# Define paths: recordings folder inside current working directory
CURRENT_DIR = os.getcwd()
RECORDINGS_DIR = os.path.join(CURRENT_DIR, "recordings")
os.makedirs(RECORDINGS_DIR, exist_ok=True)

# Define solfège notes and their standard frequencies (in Hz)
solfege_notes = {
    'Do': 261.63,
    'Re': 293.66,
    'Mi': 329.63,
    'Fa': 349.23,
    'Sol': 392.00,
    'La': 440.00,
    'Si': 493.88
}

# Filenames for individual recordings, combined audio, and embedding (all stored in RECORDINGS_DIR)
recording_files = {note: os.path.join(RECORDINGS_DIR, f"user_{note}.wav") for note in solfege_notes}
combined_audio_file = os.path.join(RECORDINGS_DIR, "combined_solfeggio2.wav")
embedding_file = os.path.join(RECORDINGS_DIR, "solfeggio_embedding2.npy")

def record_note(note, filename, duration=3, samplerate=44100):
    """Record a single solfège note and save it to a file."""
    print(f"Recording {note}... Please sing now!")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    sf.write(filename, audio_data, samplerate)
    print(f"Saved: {filename}")

def record_all_notes():
    """Record all solfège notes (Do, Re, Mi, Fa, Sol, La, Si)."""
    for note, filename in recording_files.items():
        record_note(note, filename)

def combine_audio():
    """Combine the individual note recordings into one audio file with brief pauses between them."""
    combined = AudioSegment.silent(duration=500)  # initial silence (in ms)
    for note in solfege_notes:
        filepath = recording_files[note]
        if os.path.exists(filepath):
            sound = AudioSegment.from_wav(filepath)
            # Add the sound plus a 300ms pause after each note
            combined += sound + AudioSegment.silent(duration=300)
        else:
            print(f"Warning: {filepath} not found!")
    combined.export(combined_audio_file, format="wav")
    print(f"Combined audio saved as {combined_audio_file}")

def detect_pitch(filename):
    """
    Detect the average pitch of an audio file using librosa.pyin.
    Adjust fmin and fmax to [C3, C6] (approx. 130Hz to 1046Hz) to reduce octave errors.
    """
    # Load audio at 44100 Hz
    y, sr = librosa.load(filename, sr=44100)
    # Use pyin with adjusted frequency bounds
    fmin = librosa.note_to_hz('C3')  # ~130 Hz
    fmax = librosa.note_to_hz('C6')  # ~1046 Hz
    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=fmin, fmax=fmax, sr=sr, pad_mode='constant')
    
    # Remove NaN values and take the median pitch (more robust than mean)
    valid_f0 = f0[~np.isnan(f0)]
    if len(valid_f0) == 0:
        print(f"No pitch detected in {filename}.")
        return None
    avg_pitch = np.median(valid_f0)
    
    # (Optional hack: if the detected pitch is still very low, multiply by 2)
    if avg_pitch < 150:  # adjust threshold as needed
        avg_pitch *= 2
    return avg_pitch

def map_pitch_to_note(pitch):
    """Map a detected pitch to the closest solfège note based on standard frequencies."""
    if pitch is None:
        return None
    return min(solfege_notes, key=lambda note: abs(solfege_notes[note] - pitch))

def analyze_recordings():
    """Analyze each individual recording: detect its pitch and map it to a solfège syllable."""
    print("Analyzing recorded notes...")
    for note, filename in recording_files.items():
        if os.path.exists(filename):
            pitch = detect_pitch(filename)
            mapped_note = map_pitch_to_note(pitch)
            if pitch is not None:
                print(f"{note}: Detected pitch = {pitch:.2f} Hz, Mapped to: {mapped_note}")
            else:
                print(f"{note}: No pitch detected.")
        else:
            print(f"File {filename} not found!")

def generate_embedding():
    if not os.path.exists(combined_audio_file):
        print(f"Error: {combined_audio_file} not found!")
        return
    print("Generating voice embedding...")
    # Load the combined audio at 16kHz (as expected by resemblyzer)
    wav, sr = librosa.load(combined_audio_file, sr=16000)
    encoder = VoiceEncoder()
    embedding = encoder.embed_utterance(wav)
    np.save(embedding_file, embedding)
    print(f"Voice embedding saved as {embedding_file}")

def main():
    print("Starting the full process...")
    record_all_notes()
    combine_audio()
    analyze_recordings()
    generate_embedding()
    print("Process complete! Your voice embedding is ready.")

if __name__ == "__main__":
    main()
