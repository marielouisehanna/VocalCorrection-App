import librosa
import numpy as np
"""AVANT DE CONTINUER, LIRE C'EST QUOI MFCC:
MFCCs (Mel-frequency cepstral coefficients)

 chatgpt definition : 
 MFCCs are a representation of the short-term power spectrum of an audio
 signal, commonly used in speech and voice recognition tasks.
 They capture the timbral characteristics of the voice and are very useful for voice
 identification.

 Comment on fait ca :
 librosa.load() va load user_voice.wav avec un "sampling rate" de 44100 Hz
 librosa.feature.mfcc() va tirer 13 MFCC du audio data
 np.mean() va prendre la moyenne de chacune de ces 13 MFCC sur le long du voice et va creer
 un array de 13 elements qui va representer les MFCC features (et donc les characteristiques
 uniques) de la voix de l'utilisateur.

 Pourquoi on utilise MFCC et a quoi cela peut servir:
 Les features du MFCC vont etre le "fingerprint" de la voix du user.
 Ce fingerprint est unique pour chaque user et il va nous permettre d'ajuster le pitch, la
 tonalite et d'autres caracteristiques de la voix pour pouvoir la corriger et y travailler.
 aussi, on peut utiliser, si on a besoin apres, ces features pour identifier et differencier
 les users.
"""
def extract_mfcc(filename="user_voice.wav"):
    y, sr = librosa.load(filename, sr=44100)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)  # 13 MFCC coefficients
    mfcc_mean = np.mean(mfcc, axis=1)  # Take the average
    return mfcc_mean

# Test it
mfcc_features = extract_mfcc()
print("MFCC Features:", mfcc_features)
