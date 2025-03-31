import librosa
import soundfile as sf

def shorten_song(file_path, duration=20):
    # Load the first 20 seconds of the audio file
    audio, sr = librosa.load(file_path, sr=None, duration=duration)
    
    # Overwrite the original file with shortened version
    sf.write(file_path, audio, sr, subtype='PCM_16')  # Change subtype if needed

# Example usage:
shorten_song("vocals.wav")  # Replace with your file path