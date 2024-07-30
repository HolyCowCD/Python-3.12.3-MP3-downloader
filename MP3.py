from colorama import Style, Fore, init  # for color
from yt_dlp import YoutubeDL  # for downloading from YouTube
from mutagen.id3 import ID3, ID3NoHeaderError, TIT2, TPE1, TALB, APIC  # for metadata
from mutagen.mp3 import MP3
import traceback  # for error handling
from moviepy.editor import VideoFileClip  # for conversion
import os
from PIL import Image
import requests  # for downloading the thumbnail
import time

init(autoreset=True)  # Initialize colorama
save = r"c:\Users\uujja\Downloads"  # this is where the files get saved
links = [] #? stores all the links
errors = [] #? stores all the links that got an error

def grint(text):
    print(Fore.GREEN + text + Style.RESET_ALL)

def print_info(label, info):
    print(Fore.CYAN + label + ": " + Style.BRIGHT + Fore.WHITE + str(info) + Style.RESET_ALL)

def download_video(url, output_path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'), # no clue what dis does :/
        'quiet': True # also no clue lol
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
    return info_dict

def mp3_download(link):
    try:
        video_info = download_video(link, save)
        
        # Just here incase I need to use later
        title = video_info.get('title')
        author = video_info.get('uploader')
        views = video_info.get('view_count')
        length = video_info.get('duration')
        thumbnail_url = video_info.get('thumbnail')
        mp4_path = os.path.join(save, f"{title}.mp4")

        print_info("Title", title)
        print_info("Author", author)
        print_info("Views", views)
        print_info("Length", length)

        grint("Mp4 downloaded with no metadata!")

        # Converting to mp3
        mp3_filename = f"{title}.mp3"
        mp3_path = os.path.join(save, mp3_filename)
        video_clip = VideoFileClip(mp4_path)
        video_clip.audio.write_audiofile(mp3_path)
        video_clip.close()
        grint("MP3 ready for metadata :)")

        # Adding metadata
        try:
            audio = ID3(mp3_path)
        except ID3NoHeaderError:
            audio = ID3()

        audio.add(TIT2(encoding=3, text=title))  # Title
        audio.add(TPE1(encoding=3, text=author))  # Artist
        audio.add(TALB(encoding=3, text=title))  # Album

        audio.save()

        # Download the thumbnail image
        thumbnail_png_path = os.path.join(save, "thumbnail.png")
        thumbnail_jpg_path = os.path.join(save, "thumbnail.jpg")

        response = requests.get(thumbnail_url)
        with open(thumbnail_png_path, 'wb') as file:
            file.write(response.content)
        
        try:
            with Image.open(thumbnail_png_path) as img:
                img = img.convert("RGB")
                img.save(thumbnail_jpg_path, "JPEG")
            print(f"Thumbnail converted to {thumbnail_jpg_path}")
        except Exception as e:
            print("An error occurred while converting the thumbnail:")
            traceback.print_exc()

        # Add the album cover image
        audio = MP3(mp3_path, ID3=ID3)
        with open(thumbnail_jpg_path, 'rb') as img_file:
            audio.tags.add(
                APIC(
                    encoding=3,
                    mime="image/jpeg",  # Changed to image/jpeg for .jpg
                    type=3,
                    desc='Cover',
                    data=img_file.read()
                )
            )

        # Save the audio with the new tags
        audio.save(v2_version=3)
        grint("Metadata and thumbnail added :)")
        grint("MP3 Downloaded!")

        # Clean up
        os.remove(mp4_path)
        os.remove(thumbnail_png_path)
        os.remove(thumbnail_jpg_path)
        grint("Clean up finished")

        if link in errors:
            errors.remove(link)

    except Exception as e:
        errors.append(link)

        print(Fore.RED + f"Something went wrong!: {e}")
        print(traceback.format_exc() + Style.RESET_ALL)
        input("Press enter to continue!")
    os.system('cls')

while True: #? keeps addings all the links until you done
    #Todo: make it creast the mp3 file straight up and then write to it
    print("Enter nothing to continue")
    yt_link = input(Fore.WHITE + "Enter YouTube link: " + Style.RESET_ALL)

    if len(yt_link) == 0: 
        break
    elif yt_link in links:
        print("Link has already been given!")  
        time.sleep(0.5)
    else:
        links.append(yt_link)

    os.system('cls')

for link in links:  # Loops until the program is shut
    mp3_download(link)

input("Press enter to go through the links thats had issues, exit to exit")

for link in errors: # goes through the errors again just in case
    mp3_download(link)
