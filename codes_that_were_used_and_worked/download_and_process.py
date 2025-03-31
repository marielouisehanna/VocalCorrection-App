import os
import multiprocessing
import yt_dlp as youtube_dl
from spleeter.separator import Separator

# Multiprocessing support for Windows
def freeze_support():
    multiprocessing.freeze_support()

# ---------------------
# PATHS & CONFIGURATION
# ---------------------
BASE_DIR = r"C:\Users\marie\OneDrive\Desktop\mdptest\pitch_corrector\data"
RAW_DIR = os.path.join(BASE_DIR, "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
URLS_FILE = "urls.txt"

# Create directories if they don't exist
for p in [RAW_DIR, PROCESSED_DIR]:
    os.makedirs(p, exist_ok=True)

def download_youtube_audio(url):
    """Download YouTube audio as a WAV file."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(RAW_DIR, '%(title)s.%(ext)s'),
        'verbose': True
    }
    
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            wav_path = filename.replace('.webm', '.wav').replace('.m4a', '.wav')

            if os.path.exists(wav_path):
                print(f"✅ Downloaded: {wav_path}")
                return wav_path, info['title']
            raise FileNotFoundError(f"Downloaded file not found: {wav_path}")
    except Exception as e:
        print(f"❌ Download failed: {str(e)}")
        return None, None

def extract_vocals(input_path, song_title):
    """Extract vocals using Spleeter directly to processed folder."""
    # Create a local Separator to avoid multiprocessing issues
    local_separator = Separator('spleeter:2stems')
    
    try:
        # Clean title for filename
        clean_title = "".join(c for c in song_title if c.isalnum() or c in (' ', '_')).rstrip()
        
        # Separate and save directly to processed directory
        local_separator.separate_to_file(input_path, PROCESSED_DIR)
        
        # Rename vocals file to title_vocals.wav
        old_vocals = os.path.join(PROCESSED_DIR, "vocals.wav")
        new_vocals = os.path.join(PROCESSED_DIR, f"{clean_title}_vocals.wav")
        
        os.rename(old_vocals, new_vocals)
        
        # Remove accompaniment file if it exists
        accompaniment = os.path.join(PROCESSED_DIR, "accompaniment.wav")
        if os.path.exists(accompaniment):
            os.remove(accompaniment)
        
        print(f"🎙️ Extracted vocals to: {new_vocals}")
        return new_vocals
    
    except Exception as e:
        print(f"❌ Vocal extraction failed: {str(e)}")
        return None

def process_url(url):
    """Full processing pipeline for one URL."""
    print(f"\n=== Processing: {url} ===")
    
    # Download raw audio
    raw_path, song_title = download_youtube_audio(url)
    if not raw_path:
        return None
    
    # Extract vocals with song title
    vocal_path = extract_vocals(raw_path, song_title)
    if not vocal_path:
        return None
    
    return vocal_path

def main():
    freeze_support()  # Important for Windows multiprocessing
    
    if not os.path.exists(URLS_FILE):
        print(f"Missing {URLS_FILE} file! Please create it with one URL per line.")
        return

    with open(URLS_FILE, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"🚩 Found {len(urls)} URL(s) to process\n")
    
    # Process each URL
    for url in urls:
        process_url(url)

    print("\n=== ALL DONE ===")

if __name__ == '__main__':
    main()