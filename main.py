# StageMusicBot - https://discord.gg/qBq2WSsgvv
import asyncio
import json
import logging
import os
import random
import eyed3
import time
import discord
from mutagen.easyid3 import EasyID3
from discord.ext import commands
from discord.ext.commands.errors import CommandInvokeError
from src import get_info
import config
from keep_alive import keep_alive
from dotenv import load_dotenv
load_dotenv()

from pathlib import Path



dotenv_path = Path('path/to/.env')
load_dotenv(dotenv_path=dotenv_path)

os.getenv('TOKEN')
os.getenv('MOD_ROLE')
os.getenv('GUILD_IDS')



logging.basicConfig(level=logging.WARNING, filename="main.log", filemode="w")

guilds = []
directory = os.getcwd()

if os.path.exists("./albumart.json"):
    with open("./albumart.json", "r") as cjson:
        albumart = json.load(cjson)
else:
    albumart = None

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(config.PREFIX),
    intents=discord.Intents.all(),
)


@bot.event
async def on_ready():
    global save_guild
    if not os.path.exists("./songs"):
        logging.warning(
            'Unable to find "songs" directory. Please ensure there is a "songs" directory present at the same level as this file'
        )
        return
    logging.warning(f"{bot.user} has connected to Discord!")
    while len(guilds) < 1:
        async for guild in bot.fetch_guilds(limit=5):
            save_guild = guild
            guilds.append(guild.name)
    text_channel_list = []
    for guild in bot.guilds:
        for channel in guild.stage_channels:
            text_channel_list.append(channel)
    stage = discord.utils.get(text_channel_list, name=config.STAGENAME)
    channel = stage.name
    global Vc
    global Tune
    try:
        Vc = await stage.connect()
        member = stage.guild.me
        await member.edit(suppress=False)
    except CommandInvokeError:
        pass
    while True:
        while Vc.is_playing():
            await asyncio.sleep(1)
        else:
            Tune = get_info.write_song()
            Vc.play(discord.FFmpegPCMAudio(f"songs/{Tune}"))
            Vc.cleanup()
            audiofile = EasyID3(f"songs/{Tune}")
            title = audiofile["title"][0]
            await bot.change_presence(activity=discord.Game(name=f"{title}"))
            Vc.source = discord.PCMVolumeTransformer(Vc.source, volume=config.VOLUME)
            if "suppress=False" in str(stage.voice_states):
                pass
            else:
                await member.edit(suppress=False)


@bot.command(name="close")
async def close(ctx):
    logging.warning("Shutting down via command")
    logging.shutdown()
    await bot.close()


@bot.command(
    name="nowplaying",
    description="Command to check what song is currently playing",
    aliases=["np"],
)
async def nowplaying(ctx):
    try:
        if not Vc.is_playing():
            await ctx.reply("I need to play something first")
    except:
        await ctx.reply("I need to play something first")
    else:
        song_info = get_info.info(Tune)
        embed = discord.Embed(color=0xC0F207)
        embed.set_author(name="Now Playing 🎶", icon_url=ctx.guild.icon_url).add_field(
            name="Playing", value=f"{song_info[1]} - {song_info[0]}", inline=False
        ).set_footer(
            text="This bot is still in development, if you have any queries, please contact the owner",
            icon_url=(ctx.message.author.avatar_url),
        )
        if song_info[2] is not None:
            embed.add_field(name="Album", value=f"{song_info[2]}", inline=True)
            if albumart is not None:
                try:
                    embed.set_thumbnail(url=albumart[song_info[2]])
                except KeyError:
                    logging.warning("No Albumart found")
                    pass
        else:
            pass
        await ctx.reply(embed=embed)



keep_alive()
bot.run(os.getenv("TOKEN"), reconnect=True)
