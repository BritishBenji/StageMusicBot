# StageMusicBot
Disclaimer: This Project was originally made to suit the needs of a single server, at the moment, some tweaks will be required to make it work for yours

[![Python version](https://img.shields.io/badge/python-3.9-blue.svg)](https://python.org)
![GitHub Repo stars](https://img.shields.io/github/stars/BritishBenji/StageMusicBot)
![GitHub last commit](https://img.shields.io/github/last-commit/BritishBenji/StageMusicBot)

This bot is made to sit in a Stage Channel, and play music from your local machine 24/7, simple as that!



## How to Install: 

Please try to follow these instructions first, if find that there is something you are unsure on, feel free to contact me on Discord (`BritishBenji#6321`) or open an issue, and I'll be more than happy to help.

There are a few requirements needed before you can run this bot, run the commands below to install these pre-requisits:
```py
pip install discord
pip install discord[voice]
pip install eyed3
```
After that, you're good to begin configuration!

## Configuration
At the moment, configuring the bot is a little harder than it should be, I didn't make this to be shifted from server to server easily.
But, should you wish to configure it yourself:

Make a file called `Token.txt` - In this file, paste your bot token taken from https://discord.com/developers/applications

### Edit `main.py` - 

Here, you can replace anything labeled with "Radio Striling", Line 48 can be changed so that it directs itself to whatever you have named your Stage Channel.
The Activity URL can be changed to point to your Twitch account (check correct availabilty [here](https://discordpy.readthedocs.io/en/stable/api.html?highlight=activity#activity)

### Import your songs

To import your songs, it's simple! Put all your music into a folder called `songs` in the same directory as the program, and it'll automatically read them from there! (Please note, the "now playing" command reads from ID3 tags, so these will need to be filled out for that command to pull information)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
