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


init(autoreset=True)  # Initialize colorama
save = Path(r"c:/Users/uujja/Downloads")

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
            'format': 'bestaudio/best',  # Only download the best audio
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
            'verbose': True  # I think it shows more stuff :O
        }

        with YoutubeDL(ydl_opts) as ydl:
            mp3_info = ydl.extract_info(link, download=True)
            mp3_path = Path(ydl.prepare_filename(mp3_info)).with_suffix('.mp3')

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

def main():
    while True:
        links = []  # All links given by the user
        errors = []  # Links that had issues
        
        while True:  # Asks until user has entered all links
            clear_screen()
            print("Enter nothing to continue")
            link = input(Fore.WHITE + "Enter YouTube link: " + Style.RESET_ALL)

            if not link:
                break
            elif link in links:
                print(Fore.YELLOW + "Link has already been given!")
                time.sleep(0.5)
            else:
                links.append(link)
        
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
    main()
