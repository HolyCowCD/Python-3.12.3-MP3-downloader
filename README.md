# YouTube MP3 Downloader

This project is a YouTube MP3 downloader built using Python. It downloads audio from YouTube videos, converts them to MP3 format, adds metadata, and embeds the video thumbnail as album art. It also provides a title queue feature, allowing users to track and manage downloads dynamically.

## Features

- Downloads the best available audio from YouTube videos.
- Converts downloaded audio to MP3 format.
- Adds metadata, including title, artist, views, and duration.
- Embeds the video thumbnail as album art in the MP3 file.
- Displays a dynamic queue of song titles for easier download management.
- Multithreaded fetching of video titles for quicker title updates.
- Error handling and retry for interrupted downloads.
- User-friendly interface with color-coded output for readability.

## Requirements

- **Python 3.x**
- **Packages**:
  - `yt-dlp` – for downloading YouTube videos
  - `requests` – for handling thumbnail downloads
  - `Pillow` (PIL) – for image processing
  - `mutagen` – for embedding metadata and album art in MP3 files
  - `colorama` – for colored console output
  - `pathlib` – for handling file paths (standard library in Python 3.4+)
  - `threading` and `sys` – for multithreading and system interaction (standard libraries)

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

2. Enter the YouTube video URLs when prompted. Each entry adds a title placeholder in the queue, which updates when the title is fetched. Press Enter with an empty input to start downloading.

3. The downloaded MP3 files will be saved in the specified `save` directory.

## Customization

- You can change the download directory by modifying the `save` variable in the script.
- The script is configured to download the best available audio format. You can change the quality settings by modifying the `ydl_opts` dictionary in the `download` function.

## Troubleshooting

- If the script encounters any errors while downloading or processing a link, it will retry the link after displaying an error message.
- Ensure that you have a stable internet connection and the required permissions to write to the specified download directory.

