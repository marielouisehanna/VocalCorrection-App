import os
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
from resemblyzer import VoiceEncoder
import numpy as np
import librosa

# Set up directories
RECORDINGS_DIR = "recordings"
os.makedirs(RECORDINGS_DIR, exist_ok=True)

# Solfège syllables & their frequencies
solfeggio = {
    'Do': 261.63, 'Re': 293.66, 'Mi': 329.63,
    'Fa': 349.23, 'Sol': 392.00, 'La': 440.00, 'Si': 493.88
}

combined_audio_path = os.path.join(RECORDINGS_DIR, "combined_solfeggio.wav")
embedding_path = os.path.join(RECORDINGS_DIR, "solfeggio_embedding.npy")


def record_note(syllable, filename, duration=3, samplerate=44100):
    """Records a single solfège note"""
    print(f"🎙️ Recording {syllable}... Sing now!")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    sf.write(filename, audio_data, samplerate)
    print(f"✅ Saved: {filename}")


def record_all_notes():
    """Records all solfège notes and saves them"""
    for syllable in solfeggio.keys():
        record_note(syllable, os.path.join(RECORDINGS_DIR, f"user_{syllable}.wav"))


def combine_audio():
    """Combines all recorded notes into one audio file"""
    combined = AudioSegment.silent(duration=500)  # Start with silence

    for note in solfeggio.keys():
        file_path = os.path.join(RECORDINGS_DIR, f"user_{note}.wav")
        if os.path.exists(file_path):
            sound = AudioSegment.from_wav(file_path)
            combined += sound + AudioSegment.silent(duration=300)
        else:
            print(f"⚠️ Warning: {file_path} not found!")

    combined.export(combined_audio_path, format="wav")
    print(f"✅ Combined audio saved as {combined_audio_path}")


def detect_pitch(filename):
    """Detects pitch (frequency) from an audio file"""
    y, sr = librosa.load(filename, sr=44100)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    
    pitch_values = pitches[magnitudes.argmax(axis=0), range(pitches.shape[1])]
    pitch_values = pitch_values[pitch_values > 0]  # Remove zero values
    
    if len(pitch_values) == 0:
        return None  # No pitch detected
    
    return np.mean(pitch_values)  # Average pitch detected


def map_pitch_to_note(pitch):
    """Maps detected pitch to the closest solfège note"""
    return min(solfeggio.keys(), key=lambda note: abs(solfeggio[note] - pitch))


def analyze_recordings():
    """Detects pitch for each recorded note and maps it to a solfège syllable"""
    print("🔍 Analyzing recorded notes...")

    for syllable in solfeggio.keys():
        file_path = os.path.join(RECORDINGS_DIR, f"user_{syllable}.wav")
        if os.path.exists(file_path):
            detected_pitch = detect_pitch(file_path)
            if detected_pitch:
                detected_note = map_pitch_to_note(detected_pitch)
                print(f"🎵 {syllable}: Detected Pitch = {detected_pitch:.2f} Hz, Mapped to: {detected_note}")
            else:
                print(f"⚠️ {syllable}: No pitch detected.")
        else:
            print(f"⚠️ {file_path} not found!")


def generate_embedding():
    """Processes the combined audio and creates an embedding"""
    if not os.path.exists(combined_audio_path):
        print("❌ Error: Combined audio file not found!")
        return

    print("🔄 Generating voice embedding...")
    wav, sr = librosa.load(combined_audio_path, sr=16000)
    encoder = VoiceEncoder()
    embedding = encoder.embed_utterance(wav)

    np.save(embedding_path, embedding)
    print(f"✅ Embedding saved at {embedding_path}")


# Run everything in sequence
print("🎤 Starting full process...")
record_all_notes()
combine_audio()
analyze_recordings()
generate_embedding()
print("🚀 Process complete! Your voice embedding is ready.")
