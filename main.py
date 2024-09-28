import os
import yt_dlp

def sanitize_filename(filename):
    """Replace illegal characters in filename."""
    return filename.replace(':', '').replace('?', '').replace('/', '_').replace('\\', '_').replace(' ', '_')

def download_youtube(url, output_path, output_format):
    if output_path is None:
        output_path = os.path.join(os.path.expanduser('~'), 'C:\\YTtoMP3')  # Default to YTtoMP3 folder

    try:
        os.makedirs(output_path, exist_ok=True)

        # ydl_opts with format option included
        if output_format == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(output_path, f"{sanitize_filename('%(title)s.%(ext)s')}"),
                'ffmpeg_location': r'C:\ffmpeg\bin',
                'verbose': True,
            }
        elif output_format == 'mp4':
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                'outtmpl': os.path.join(output_path, f"{sanitize_filename('%(title)s.%(ext)s')}"),
                'ffmpeg_location': r'C:\ffmpeg\bin',
                'verbose': True,
            }
        else:
            print("Invalid format selected.")
            return

        print(f"Output path template: {ydl_opts['outtmpl']}")  # Print the template for debugging

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading: {url}")
            ydl.download([url])

        print("Download complete!")

        # Generate the expected file name
        video_info = ydl.extract_info(url, download=False)
        expected_title = sanitize_filename(video_info['title'])
        expected_file_name = os.path.join(output_path, f"{expected_title}.{output_format}")

        print(f"Expected file path: {expected_file_name}")

        if os.path.exists(expected_file_name):
            print(f"File found at: {expected_file_name}")
        else:
            print("File not found!")
            print("Files in directory:")
            print(os.listdir(output_path))

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    url = input("Enter the YouTube URL: ")
    filepath = input("Enter the output filepath: ")
    format_choice = input("Type the format (mp3/mp4): ").strip().lower()

    if format_choice in ['mp3', 'mp4']:
        download_youtube(url, filepath, format_choice)
    else:
        print("Invalid format choice! Please enter 'mp3' or 'mp4'.")
