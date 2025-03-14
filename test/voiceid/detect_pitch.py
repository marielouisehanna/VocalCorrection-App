import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

def detect_pitch(filename="user_note.wav"):
    """
    Detects the pitch (frequency) from an audio file.
    :param filename: The path to the audio file.
    :return: The detected pitch in Hz.
    """
    # Load the audio file
    y, sr = librosa.load(filename, sr=44100)
    
    # Use PyIN (Pitch Estimation) to detect the pitch
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
    
    # Find the index of the maximum magnitude in each time frame
    pitch_indices = magnitudes.argmax(axis=0)  # Index of the max magnitude per time frame
    
    # Get the pitch corresponding to this maximum magnitude in each time frame
    pitch_values = pitches[pitch_indices, range(pitches.shape[1])]
    
    # Filter out any zero values (which indicate no pitch detected)
    pitch_values = pitch_values[pitch_values > 0]
    
    if len(pitch_values) == 0:
        print("No valid pitch detected.")
        return None
    
    # Get the average pitch (since multiple time frames are processed)
    avg_pitch = np.mean(pitch_values)
    
    print(f"Detected pitch: {avg_pitch} Hz")
    
    # Plot the waveform of the audio
    plt.figure(figsize=(10, 6))
    librosa.display.waveshow(y, sr=sr)
    plt.title(f"Waveform of {filename}")
    plt.show()
    
    return avg_pitch

# Test pitch detection with one example
detect_pitch("user_Do.wav")
