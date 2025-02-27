import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers # type: ignore
import librosa
import soundfile as sf

# Load audio function
def load_audio(file_path, sr=16000):
    audio, _ = librosa.load(file_path, sr=sr)
    return audio

# Wave-U-Net Architecture
def build_wave_unet(input_shape):
    inputs = keras.Input(shape=input_shape)

    # Encoder
    x1 = layers.Conv1D(64, kernel_size=15, strides=1, padding="same", activation="relu")(inputs)
    x2 = layers.MaxPooling1D(pool_size=2)(x1)
    x3 = layers.Conv1D(128, kernel_size=15, strides=1, padding="same", activation="relu")(x2)
    x4 = layers.MaxPooling1D(pool_size=2)(x3)
    
    # Bottleneck
    bottleneck = layers.Conv1D(256, kernel_size=15, strides=1, padding="same", activation="relu")(x4)

    # Decoder
    x5 = layers.UpSampling1D(size=2)(bottleneck)
    x6 = layers.Concatenate()([x5, x3])
    x7 = layers.Conv1D(128, kernel_size=15, strides=1, padding="same", activation="relu")(x6)
    
    x8 = layers.UpSampling1D(size=2)(x7)
    x9 = layers.Concatenate()([x8, x1])
    x10 = layers.Conv1D(64, kernel_size=15, strides=1, padding="same", activation="relu")(x9)
    
    outputs = layers.Conv1D(1, kernel_size=1, strides=1, padding="same")(x10)
    model = keras.Model(inputs=inputs, outputs=outputs)
    return model

# Compile and Train Model
def train_wave_unet():
    model = build_wave_unet(input_shape=(None, 1))
    model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mae"])

    mixed_dir = "ml_models/noise_removal/data/mixed"
    clean_dir = "ml_models/noise_removal/data/clean"

    mixed_files = sorted([os.path.join(mixed_dir, f) for f in os.listdir(mixed_dir)])
    clean_files = sorted([os.path.join(clean_dir, f) for f in os.listdir(clean_dir)])

    # Training Loop
    for epoch in range(10):  # Adjust number of epochs
        for mixed_file, clean_file in zip(mixed_files, clean_files):
            mixed = load_audio(mixed_file).reshape(-1, 1)
            clean = load_audio(clean_file).reshape(-1, 1)

            # Train on batch
            model.train_on_batch(np.expand_dims(mixed, axis=0), np.expand_dims(clean, axis=0))

        # Save model checkpoints
        if (epoch + 1) % 5 == 0:
            model.save(f"ml_models/noise_removal/models/wave_unet_epoch_{epoch+1}.h5")
            print(f"Model checkpoint saved at epoch {epoch+1}")

if __name__ == "__main__":
    train_wave_unet()
