from discord.ext import commands
import eyed3
import random
import os


def info(Tune):
    audiofile = eyed3.load(f"songs/{Tune}")
    artist = audiofile.tag.artist
    title = audiofile.tag.title
    album = audiofile.tag.album
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
