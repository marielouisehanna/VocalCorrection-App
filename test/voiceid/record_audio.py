import sounddevice as sd #to record the voice
import soundfile as sf

def record_audio(filename="user_voice.wav", duration=5, samplerate=44100): #record voice de 5 sec
    print("Recording... Speak now!")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait() #until the recording is finished
    sf.write(filename, audio_data, samplerate)
    print(f"Recording saved as {filename}")

# Call the function to test recording
record_audio()