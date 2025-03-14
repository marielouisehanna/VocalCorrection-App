import yt_dlp
import ffmpeg
import os

def download_youtube_audio(url):
    save_path = r"C:\Users\f\Desktop\chiara\2025\univ\MDP\VocalCorrection-App\uploads"  # Directory to save the file

    if not os.path.exists(save_path):
        os.makedirs(save_path)  # Ensure the directory exists

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'aac',  # Download as M4A audio
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),  # Save the file in the specified directory
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        return os.path.join(save_path, ydl.prepare_filename(info_dict).replace('.webm', '.m4a'))  # Ensure it's M4A

##def convert_m4a_to_mp3(input_file, output_file):
##    ffmpeg.input(input_file).output(output_file, acodec='libmp3lame', ab='192k').run()

if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    filepath = download_youtube_audio(url)
    print(f"Downloaded audio file: {filepath}")

##    input_file = filepath  # Path to your M4A file
##    output_file = filepath.replace('.m4a', '.mp3')  # Convert to MP3 with the same filename

##    convert_m4a_to_mp3(input_file, output_file)
##    print(f"Conversion complete: {output_file}")
