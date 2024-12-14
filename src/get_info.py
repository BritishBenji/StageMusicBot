import mutagen, random, os

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


def info(Tune):
    audiofile = MP3(f"songs/{Tune}", ID3=EasyID3)
    album = audiofile["album"][0]
    title = audiofile["title"][0]
    artist = audiofile["performer"][0]
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
