import sounddevice as sd
import soundfile as sf
import numpy as np
import time
from queue import Queue
from threading import Event
import librosa

class LiveVocalRecorder:
    def __init__(self, song_path):
        # Audio configuration
        self.sample_rate = 44100
        self.duration = 20  # seconds
        self.dtype = 'float32'
        
        # Load and prepare first 20s of song
        self.song_audio, _ = librosa.load(
            song_path,
            sr=self.sample_rate,
            mono=False,
            duration=self.duration
        )
        
        # Convert to stereo if mono
        if len(self.song_audio.shape) == 1:
            self.song_audio = np.vstack([self.song_audio, self.song_audio])
        
        # Buffers and flags
        self.recording_buffer = Queue()
        self.stop_event = Event()
        
        # Latency compensation (adjust based on your hardware)
        self.latency_offset = int(0.2 * self.sample_rate)  # 200ms

    def _input_callback(self, indata, frames, time, status):
        """Microphone recording callback"""
        self.recording_buffer.put(indata.copy())

    def _output_callback(self, outdata, frames, time, status):
        """Song playback callback"""
        if self.current_position + frames > len(self.song_audio[0]):
            remaining = len(self.song_audio[0]) - self.current_position
            outdata[:remaining] = self.song_audio[:, self.current_position:].T
            outdata[remaining:] = 0
            raise sd.CallbackStop
        else:
            outdata[:] = self.song_audio[:, self.current_position:self.current_position+frames].T
            self.current_position += frames

    def _play_countdown(self):
        """3-second audio/visual countdown"""
        print("\n🎶 Starting in:")
        for i in range(3, 0, -1):
            print(f"🎤 {i}...")
            beep = librosa.tone(440, sr=self.sample_rate, duration=0.5)
            sd.play(beep, samplerate=self.sample_rate)
            time.sleep(1)
        print("\nSING NOW!\n")

    def record(self, output_path):
        # Initialize streams
        input_stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            callback=self._input_callback,
            blocksize=1024
        )

        output_stream = sd.OutputStream(
            samplerate=self.sample_rate,
            channels=2,
            callback=self._output_callback,
            finished_callback=self.stop_event.set
        )

        # Reset position tracker
        self.current_position = 0

        # Start countdown
        self._play_countdown()

        # Start recording and playback
        input_stream.start()
        output_stream.start()

        try:
            # Wait for playback to complete
            while not self.stop_event.is_set():
                time.sleep(0.1)
            
            # Wait for remaining audio to flush
            time.sleep(0.5)

        finally:
            # Stop streams
            input_stream.stop()
            output_stream.stop()
            input_stream.close()
            output_stream.close()

            # Process recording
            recorded_chunks = []
            while not self.recording_buffer.empty():
                recorded_chunks.append(self.recording_buffer.get())
            
            if recorded_chunks:
                raw_vocals = np.concatenate(recorded_chunks)
                
                # Apply latency compensation
                if len(raw_vocals) > self.latency_offset:
                    raw_vocals = raw_vocals[self.latency_offset:]
                
                # Trim to exact duration
                max_samples = self.duration * self.sample_rate
                raw_vocals = raw_vocals[:max_samples]
                
                # Save files
                sf.write(output_path, raw_vocals, self.sample_rate)
                sf.write("reference_track_20s.wav", self.song_audio.T, self.sample_rate)
                
                print(f"\n✅ 20s recording saved to {output_path}")
                print("✅ 20s reference track saved to reference_track_20s.wav")
            else:
                print("\n❌ No audio was recorded - check your microphone!")

if __name__ == "__main__":
    # ======================================
    # EDIT THESE FILENAMES BEFORE RUNNING
    input_song = "vocals.wav"  # Your input song file
    output_vocals = "kebrit.wav"  # Where to save your vocals
    # ======================================
    
    recorder = LiveVocalRecorder(input_song)
    recorder.record(output_vocals)