from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import librosa
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the audio file
wav_path = os.path.join(script_dir, "sweet-soul-siren-climactic-rn-b-loop_142bpm_C_minor.wav")  # Ensure the correct path
wav, sr = librosa.load(wav_path, sr=16000)

# Process the audio and extract speaker embedding
encoder = VoiceEncoder()
embedding = encoder.embed_utterance(wav)

# Define the save path in the same directory as the script
embedding_path = os.path.join(script_dir, "sweet-soul-siren-climactic-rn-b-loop_142bpm_C_minor.wav")
np.save(embedding_path, embedding)

print(f"✅ Embedding saved at: {embedding_path}")

# Verify if the file is saved
if os.path.exists(embedding_path):
    print("✅ File successfully saved in the script's directory!")
else:
    print("❌ Error: File not found.")
