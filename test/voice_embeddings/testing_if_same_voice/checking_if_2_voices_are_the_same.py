import numpy as np
from scipy.spatial.distance import cosine, euclidean

# Load embeddings
embedding1 = np.load(r"C:\Users\marie\OneDrive\Desktop\code mdp\VocalCorrection-App\voice_embeddings\testing_if_same_voice\solfeggio_embedding2.npy")
embedding2 = np.load(r"C:\Users\marie\OneDrive\Desktop\code mdp\VocalCorrection-App\voice_embeddings\testing_if_same_voice\solfeggio_embedding.npy")

# Normalize embeddings for better accuracy
embedding1 = embedding1 / np.linalg.norm(embedding1)
embedding2 = embedding2 / np.linalg.norm(embedding2)

# Compute similarity scores
similarity = 1 - cosine(embedding1, embedding2)
distance = euclidean(embedding1, embedding2)

# Print results
print(f"🔍 Speaker Similarity Score: {similarity:.4f}")
print(f"📏 Euclidean Distance: {distance:.4f}")

# Thresholds
same_speaker_threshold = 0.85  # High confidence threshold
uncertain_threshold = 0.80  # Gray area
distance_threshold = 0.7  # Lower = more similar

# Decision logic using both similarity and distance
if similarity >= same_speaker_threshold and distance < distance_threshold:
    print("✅ Same speaker detected with high confidence!")
elif similarity >= uncertain_threshold and distance < 1.0:
    print("⚠️ Possible same speaker, but needs further verification.")
else:
    print("❌ Different speakers.")
