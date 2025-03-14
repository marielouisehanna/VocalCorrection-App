import os
import shutil
import sounddevice as sd
import wave

# Directory where the files will be saved
SAVE_PATH = r"C:\Users\f\Desktop\chiara\2025\univ\MDP\VocalCorrection-App\uploads"

# Ensure the directory exists
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

def record_audio(filename, duration, samplerate=44100):
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2, dtype='int16')
    sd.wait()  # Wait until recording is finished

    filepath = os.path.join(SAVE_PATH, filename + ".wav")

    # Save the recording
    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(recording.tobytes())

    print(f"Recording saved: {filepath}")

def upload_audio():
    file_path = input("Enter the full path of the audio file you want to upload: ").strip()
    print(f"DEBUG: User entered path -> {file_path}")

    if os.path.exists(file_path):
        filename = os.path.basename(file_path)
        destination = os.path.join(SAVE_PATH, filename)
        shutil.copy(file_path, destination)  # Copy instead of move
        print(f"File copied and saved to: {destination}")
    else:
        print("Error: File not found. Please check the path and try again.")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Record an audio")
    print("2. Upload an existing audio")

    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        duration = int(input("Enter recording duration (in seconds): ").strip())
        filename = input("Enter filename (without extension): ").strip()
        record_audio(filename, duration)
    elif choice == "2":
        upload_audio()
    else:
        print("Invalid choice! Please restart the script.")
