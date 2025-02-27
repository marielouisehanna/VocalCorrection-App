import os
import numpy as np
import librosa
import soundfile as sf

def load_audio(file_path, sr=16000):
    audio, _ = librosa.load(file_path, sr=sr)
    return audio

def mix_clean_noisy(clean_path, noise_path, snr=0):
    clean = load_audio(clean_path)
    noise = load_audio(noise_path)

    # Ensure both are the same length
    min_len = min(len(clean), len(noise))
    clean, noise = clean[:min_len], noise[:min_len]

    # Adjust noise volume to achieve the desired SNR
    noise_power = np.mean(noise ** 2)
    clean_power = np.mean(clean ** 2)
    scaling_factor = np.sqrt(clean_power / (10**(snr / 10) * noise_power))
    noisy = clean + scaling_factor * noise

    return clean, noisy

def create_noisy_dataset(clean_dir, noise_dir, output_dir, snr=0):
    clean_files = sorted([os.path.join(clean_dir, f) for f in os.listdir(clean_dir)])
    noise_files = sorted([os.path.join(noise_dir, f) for f in os.listdir(noise_dir)])

    os.makedirs(output_dir, exist_ok=True)

    for clean_file in clean_files:
        for noise_file in noise_files:
            clean, noisy = mix_clean_noisy(clean_file, noise_file, snr)
            base_name = os.path.basename(clean_file).replace('.wav', '')
            output_file = os.path.join(output_dir, f"{base_name}_noisy.wav")
            sf.write(output_file, noisy, 16000)
            print(f"Saved: {output_file}")

if __name__ == "__main__":
    create_noisy_dataset(
        clean_dir="ml_models/noise_removal/data/clean",
        noise_dir="ml_models/noise_removal/data/noisy",
        output_dir="ml_models/noise_removal/data/mixed",
        snr=0  # Change SNR value for different noise levels
    )
