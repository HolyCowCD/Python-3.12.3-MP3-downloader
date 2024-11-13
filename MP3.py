import os
from yt_dlp import YoutubeDL
import requests
from PIL import Image
import traceback
from mutagen.id3 import ID3, APIC 
from mutagen.mp3 import MP3
from colorama import Fore, Style, init
import time
from pathlib import Path
import threading
import sys

title_queue = [] # Global queue to store fetched song titles
init(autoreset=True)  # Initialize colorama

save = Path(r"")

def grint(text):
    """Output grean text"""
    print(Fore.GREEN + text + Style.RESET_ALL)

def print_info(label, info):
    """
    outputs --> cyan label: white text
    """
    print(Fore.CYAN + label + ": " + Style.BRIGHT + Fore.WHITE + info + Style.RESET_ALL)

def clear_screen():
    """clears the console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def download(link):
    """Download a video using its YouTube Link"""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',  # downloads the best audio
            'outtmpl': str(save / '%(title)s.%(ext)s'),  # Template = title.extension
            'quiet': False,  # Shows whats happening, setting to True will hide everything but thats boring
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3', 
                },
                {
                    'key': 'FFmpegMetadata',  
                    'add_metadata': True,
                }
            ],
            'verbose': False  # I think it shows more stuff :O
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            mp3_info = ydl.extract_info(link, download=True)
            name = ydl.prepare_filename(mp3_info)
            mp3_path = Path(name).with_suffix('.mp3')

        thumbnail_url = mp3_info.get('thumbnail')

        if thumbnail_url:
            try:
                # Download and convert the thumbnail image
                png_path = save / "thumbnail.png"
                jpg_path = save / "thumbnail.jpg"

                response = requests.get(thumbnail_url)
                with open(png_path, 'wb') as file:
                    file.write(response.content)
                
                with Image.open(png_path) as img:
                    img = img.convert("RGB")
                    img.save(jpg_path, "JPEG")
                grint(f"Thumbnail converted to {jpg_path}")

                # Add cover image and save
                audio = MP3(mp3_path, ID3=ID3)
                with open(jpg_path, 'rb') as img_file:
                    audio.tags.add(
                        APIC(
                            encoding=3,
                            mime="image/jpeg",
                            type=3,
                            desc='Cover',
                            data=img_file.read()
                        )
                    )
                audio.save(v2_version=3)
                grint(f"Added album art to {mp3_path}")

                # Clean up image files
                png_path.unlink()
                jpg_path.unlink()

            except Exception as e:
                print(Fore.RED + "Failed to add album art:")
                traceback.print_exc()

    except Exception as e:
        print(Fore.RED + f"Something went wrong!: {e}")
        print(traceback.format_exc() + Style.RESET_ALL)
        input("Press enter to continue!")
        return False

    return True

def fetch_title(link, index):
    """Fetches the title from a YouTube link and updates the queue."""
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True, 'format': 'bestaudio/best'}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            title = info.get('title', 'Unknown title')
    except Exception:
        title = "Failed to retrieve title"
    
    # Update the song title in the queue
    title_queue[index] = title
    update_display()  # Refresh the display with the new title

def update_display():
    """Clears the screen and displays the song title queue and input prompt."""
    clear_screen()
    
    # Display the queue of fetched titles
    print("Fetched Songs:")
    for i, title in enumerate(title_queue, start=1):
        print(f"  {i}. {title}")

    # Display the prompt for the next link
    print("\nEnter link or nothing to continue")

def main():    
    count = 1
    links = []
    errors = []

    while True:
        # Display the song queue and prompt for the next link
        update_display()

        link = input(Fore.WHITE + f"Enter song[{count}]: " + Style.RESET_ALL)
        sys.stdout.flush()

        if not link:
            break
        else:
            title_queue.append("Fetching...")# place holder
            
            # fetches in difference thread :)
            title_thread = threading.Thread(target=fetch_title, args=(link, count - 1))
            title_thread.start()

            links.append(link)
            count += 1

    # Process each link and handle errors
    for link in links:
        if not download(link):
            errors.append(link)

    if errors:
        input(Fore.RED + "Press enter to retry links that had issues, or exit to exit")
        for link in errors:
            download(link)
        clear_screen()
        print(Fore.RED + "Links that got errors:")
        for error_link in errors:
            print(Fore.RED + error_link)
    else:
        input("You can download again or exit")

if __name__ == "__main__":
    while True:
        main()
        title_queue.clear()
