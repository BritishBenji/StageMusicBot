# StageMusicBot
Disclaimer: This version of the bot was only tested on Linux, running with PM2 and restarts with a 6 hour CronoJob. It may not be suitable for normal use.

[![Python version](https://img.shields.io/badge/python-3.9-blue.svg)](https://python.org)
![GitHub Repo stars](https://img.shields.io/github/stars/BritishBenji/StageMusicBot)
![GitHub last commit](https://img.shields.io/github/last-commit/BritishBenji/StageMusicBot)

This bot is made to sit in a Stage Channel, and play music from your local machine 24/7, simple as that!



## How to Install: 

Please try to follow these instructions first, if find that there is something you are unsure on, feel free to contact me on Discord (https://discord.gg/qBq2WSsgvv) or open an issue, and I'll be more than happy to help.

There are a few requirements needed before you can run this bot, run the command below to install these pre-requisits:

Windows:
```
py -m pip install -r requirements.txt
```
Linux:
```
python3 -m pip install -r requirements.txt
```
After that, you're good to begin configuration!

## Configuration
To configure your bot, make a copy of `config.json.example`, and fill in the information there.

- `token` = Your bot token from https://discord.com/developers/applications
- `prefix` = Your chosen bot prefix for both
- `guild_id` = Currently not required
- `stage_name` = The name of the stage channel you wish for the bot to join. **NOTE: this is CaSe sensitive**
- `now_playing` = The text channel ID's of channels you want to allow users to run the `now playing` command in
- `mod_role` = The name of the role you wish to allow to run `join` or `close`. **NOTE: this is CaSe sensitive**

### Edit `main.py` - 

The only reason to currently edit `main.py` is to either allow your bot to show specific album art (see the last few lines), or to make edits/improvements to the program itself.

**LINUX USERS:**

You may need to edit `main.py` to fit your operating system's directories. *(This may just be a case of swapping backslashes for forward slashes in certain cases)*

### Import your songs

To import your songs, it's simple! Put all your music into a folder called `songs` in the same directory as the program, and it'll automatically read them from there! (Please note, the "now playing" command reads from ID3 tags, so these will need to be filled out for that command to pull information)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
