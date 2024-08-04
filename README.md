# YouTube MP3 Downloader

This project is a YouTube MP3 downloader built using Python. It downloads audio from YouTube videos, converts them to MP3 format, adds metadata, and embeds the video thumbnail as album art.

## Features

- Downloads the best available audio from YouTube videos.
- Converts downloaded audio to MP3 format.
- Adds metadata including title, artist, views, and duration.
- Embeds the video thumbnail as album art in the MP3 file.
- User-friendly interface with colored output for better readability.

## Requirements

- Python 3.x
- yt-dlp
- requests
- Pillow (PIL)
- mutagen
- colorama

## Installation

1. Clone this repository:
    ```sh
    git clone https://github.com/yourusername/yt-mp3-downloader.git
    cd yt-mp3-downloader
    ```

2. Install the required Python packages:
    ```sh
    pip install yt-dlp requests Pillow mutagen colorama
    ```

## Usage

1. Run the script:
    ```sh
    python downloader.py
    ```

2. Enter the YouTube video URLs when prompted. Press Enter with an empty input to start downloading.

3. The downloaded MP3 files will be saved in the specified `save` directory (`c:\Users\uujja\Downloads` by default).

## Customization

- You can change the download directory by modifying the `save` variable in the script.
- The script is designed to download the best available audio format. You can change the quality settings by modifying the `ydl_opts` dictionary in the `download` function.

## Troubleshooting

- If the script encounters any errors while downloading or processing a link, it will retry the link after displaying an error message.
- Ensure that you have a stable internet connection and the required permissions to write to the specified download directory.
