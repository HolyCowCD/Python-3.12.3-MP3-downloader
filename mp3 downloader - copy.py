from colorama import Style, Fore, init  # for color
from pytube import YouTube  # for downloading from YouTube
from mutagen.id3 import ID3, ID3NoHeaderError, TIT2, TPE1, TALB, APIC  # for metadata
from mutagen.mp3 import MP3
import traceback  # for error handling
from moviepy.editor import VideoFileClip  # for conversion
import os
import requests  # for downloading the thumbnail

#* https://youtu.be/dQw4w9WgXcQ?si=mf_YYbTUPXRfWBcb

init(autoreset=True) # Initialize colorama or whatever
#! change download folder if your not me :/
save = r"D:\coding crap\vscode at school"  # this is where the files get saved

#* <---------- | functions | ---------->
def clear():
    os.system('cls')

def grint(text): 
    print(Fore.GREEN + text + Style.RESET_ALL)

def print_info(label, info):
    print(Fore.CYAN + label + ": " + Style.BRIGHT + Fore.WHITE + str(info) + Style.RESET_ALL)

def display_info(link): #? just shows info abt video
    global yt #! might make script slower so learn abt how global effects performance!
    yt = YouTube(link)
    print_info("Title", yt.title)
    print_info("Author", yt.author)
    print_info("Views", yt.views)
    print_info("Length", yt.length)

def mp4(): #? downloads as mp4
    global mp4_path
    yd = yt.streams.get_highest_resolution()  # best quality for mp4
    mp4_path = yd.download(output_path=save)
    grint("Mp4 downloaded with no metadata!")

def conversion():#? Converting to mp3
    global mp3_path
    mp3_filename = yt.title + ".mp3"  #? for renaming it
    mp3_path = os.path.join(save, mp3_filename)  # download a copy at 'save' as a .mp3
    video_clip = VideoFileClip(mp4_path)  # this is to make a variable
    video_clip.audio.write_audiofile(mp3_path)  # actually downloads
    video_clip.close()  # stops the conversion
    grint("MP3 ready for metadata :)")
    
def meta_dat():#? Adding metadata
    global audio
    try:  # using the advanced format (more verstile i think)
        audio = ID3(mp3_path)
    except ID3NoHeaderError:
        audio = ID3()

    audio.add(TIT2(encoding=3, text=yt.title))  # Title
    audio.add(TPE1(encoding=3, text=yt.author))  # Artist
    audio.add(TALB(encoding=3, text=yt.title))  # Album

    audio.save() # save the tags?
    grint("meta data saved!")

def get_thumbnail(): #? Downloads the thumbnail image
    global thumbnail_path
    thumbnail_path = os.path.join(save, "thumbnail.png")  # empty image file
    response = requests.get(yt.thumbnail_url)  # writes to empty image file
    with open(thumbnail_path, 'wb') as file:
        file.write(response.content)

def add_cover():#? Adds the album cover image
    audio = MP3(mp3_path, ID3=ID3)
    with open(thumbnail_path, 'rb') as img_file:
        audio.tags.add(
            APIC(
                encoding=3,  # utf-8 cus 2^3 = 8
                mime="image/png",  # uses png, might be an issue if someone else is a png
                type=3,  # 3 = cover image :)
                desc='Cover',
                data=img_file.read() 
            )
        )


while True:  # Loops until the program is shut
    try: 
        display_info(input("Enter YouTube link: "))
        
        mp4()
        
        conversion()
        
        meta_dat()

        get_thumbnail()
        
        add_cover()

        # Save the audio with the new tags
        audio.save(v2_version=3)  # saving in ID3v2.3 format, whatever that means 
        grint("Metadata and thumbnail added :)")
        grint("MP3 Downloaded!")

        # Clean up
        os.remove(thumbnail_path)  # remove the downloaded thumbnail file
        os.remove(mp4_path)  # remove the downloaded mp4 file
        grint("Clean up finished")

    except Exception as e:
        print(Fore.RED + f"Something went wrong!: {e}")  # not very good :(
        print(traceback.format_exc() + Style.RESET_ALL)  # this gives more info

    clear()
    
    
    