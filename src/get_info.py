from discord.ext import commands
from mutagen.id3 import ID3
import mutagen
import random
import os


def info(Tune):
    audiofile = mutagen.File(f"songs/{Tune}")
    artist = audiofile["artist"][0]
    title = audiofile["title"][0]
    try:
        album = audiofile["album"][0]
    except KeyError:
        album = None
    return [artist, title, album]


def write_song():
    if not os.path.exists("./songs.txt"):
        f = open("songs.txt", "x")
        f.close()
        # If all songs played
    with open("songs.txt") as f:
        x = len(f.readlines())
    if x == len(os.listdir("songs/")):
        f = open("songs.txt", "w+")
        f.close()
    # Add song to list
    with open("songs.txt", "a+") as File:
        File.seek(0)
        played = File.readlines()
        if len(played) == 0:
            Tune = random.choice(os.listdir("songs/"))
            File.write(f"{Tune}\n")
            return Tune
        Tune = random.choice(os.listdir("songs/"))
        while f"{Tune}\n" in played:
            Tune = random.choice(os.listdir("songs/"))
        File.write(f"{Tune}\n")
        return Tune
