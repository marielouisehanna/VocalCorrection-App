import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
from resemblyzer import VoiceEncoder
import numpy as np
import librosa

# Define paths and configurations
CURRENT_DIR = os.getcwd()
RECORDINGS_DIR = os.path.join(CURRENT_DIR, "recordings")
os.makedirs(RECORDINGS_DIR, exist_ok=True)

SENTENCE = "Watan al nujoum... ana huna, haddi2... atzakar men ana? Alama7ta fi el madi el ba3id, fatan ghriran ar3ana?"

solfege_notes = {
    'Do': 261.63,  # C4
    'Re': 293.66,  # D4
    'Mi': 329.63,  # E4
    'Fa': 349.23,  # F4
    'Sol': 392.00, # G4
    'La': 440.00,  # A4
    'Si': 493.88   # B4
}

recording_files = {note: os.path.join(RECORDINGS_DIR, f"user_{note}.wav") for note in solfege_notes}
combined_audio_file = os.path.join(RECORDINGS_DIR, "ML.wav")
embedding_file = os.path.join(RECORDINGS_DIR, "ML.npy")

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

def record_sentence(filename, duration=10, samplerate=44100):
    """Record the spoken sentence"""
    print("\nNow please read this sentence:")
    print(SENTENCE)
    print("Recording starts now...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    sf.write(filename, audio_data, samplerate)
    print(f"Saved sentence recording to: {filename}")

def combine_audio():
    """Combine notes and sentence into one audio file"""
    combined = AudioSegment.silent(duration=500)
    
    # Add musical notes
    for note in solfege_notes:
        filepath = recording_files[note]
        if os.path.exists(filepath):
            sound = AudioSegment.from_wav(filepath)
            combined += sound + AudioSegment.silent(duration=300)
    
    # Add sentence recording
    sentence_path = os.path.join(RECORDINGS_DIR, "sentence.wav")
    if os.path.exists(sentence_path):
        combined += AudioSegment.silent(duration=1000)  # 1 second pause
        combined += AudioSegment.from_wav(sentence_path)
    
    combined.export(combined_audio_file, format="wav")
    print(f"Combined audio saved as {combined_audio_file}")

def detect_pitch(filename):
    """
    Detect the average pitch of an audio file using librosa.pyin.
    Adjust fmin and fmax to [C3, C6] (approx. 130Hz to 1046Hz) to reduce octave errors.
    """
    y, sr = librosa.load(filename, sr=44100)
    fmin = librosa.note_to_hz('C3')
    fmax = librosa.note_to_hz('C6')
    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=fmin, fmax=fmax, sr=sr, pad_mode='constant')
    
    valid_f0 = f0[~np.isnan(f0)]
    if len(valid_f0) == 0:
        print(f"No pitch detected in {filename}.")
        return None
    avg_pitch = np.median(valid_f0)
    
    if avg_pitch < 150:
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
    wav, sr = librosa.load(combined_audio_file, sr=16000)
    encoder = VoiceEncoder()
    embedding = encoder.embed_utterance(wav)
    np.save(embedding_file, embedding)
    print(f"Voice embedding saved as {embedding_file}")

def main():
    print("Starting the full process...")
    
    # 1. Record musical notes
    record_all_notes()
    
    # 2. Record spoken sentence
    sentence_path = os.path.join(RECORDINGS_DIR, "sentence.wav")
    record_sentence(sentence_path)
    
    # 3. Combine all audio
    combine_audio()
    
    # 4. Analyze and generate embedding
    analyze_recordings()
    generate_embedding()
    
    print("Process complete! Your combined voice embedding is ready.")

if __name__ == "__main__":
    main()