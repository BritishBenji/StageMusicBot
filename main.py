# StageMusicBot - https://discord.gg/qBq2WSsgvv
import asyncio
import json
import os
import random
import time

import discord
import eyed3
from discord import AudioSource, FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.errors import CommandInvokeError

guilds = []
directory = os.getcwd()

# collect token here#
with open('./config.json', 'r') as cjson:
    config = json.load(cjson)

if os.path.exists("./albumart.json"):
    with open('./albumart.json', 'r') as cjson:
        albumart = json.load(cjson)


def get_prefix(client, message):
    # sets the prefixes, you can keep it as an array of only 1 item if you need only one prefix
    prefixes = [config["prefix"]]

    if not message.guild:
        # Only allow '*' as a prefix when in DMs, this is optional
        prefixes = [config["prefix"]]

    return commands.when_mentioned_or(*prefixes)(client, message)


bot = commands.Bot(command_prefix=get_prefix, description="A Music Bot to play Lindsey Stirling's amazing music, 24/7, just for you!",
                   case_insensitive=True, help_command=None)

TOKEN = config["token"]


@bot.event
async def on_ready():
    if not os.path.exists("./songs"):
        print("Unable to find \"songs\" directory. Please ensure there is a \"songs\" directory present at the same level as this file")
        return
    print(f'{bot.user} has connected to Discord!')
    while len(guilds) < 1:
        async for guild in bot.fetch_guilds(limit=5):
            guilds.append(guild.name)
    print(guilds)
    text_channel_list = []
    for guild in bot.guilds:
        for channel in guild.stage_channels:
            text_channel_list.append(channel)
    stage = discord.utils.get(text_channel_list, name=config["stage_name"])
    channel = stage.name
    global Vc
    global Tune
    try:
        Vc = await stage.connect()
        member = guild.get_member(config["bot_id"])
        await member.edit(suppress=False)
    except CommandInvokeError:
        pass
    played = []
    while True:
        while Vc.is_playing():
            await asyncio.sleep(1)
        else:
            repeated = True
            while repeated:
                if len(played) > 20:
                    played = []
                Tune = random.choice(os.listdir("songs/"))
                while Tune in played:
                    Tune = random.choice(os.listdir("songs/"))
                played.append(Tune)
                repeated = False
            Vc.play(discord.FFmpegPCMAudio(f'songs/{Tune}'))
            audiofile = eyed3.load(f"songs/{Tune}")
            title = audiofile.tag.title
            await bot.change_presence(
                activity=discord.Game(name=f"{title}"))
            Vc.source = discord.PCMVolumeTransformer(Vc.source, volume=config["volume"])
            if "suppress=False" in str(stage.voice_states):
                pass
            else:
                await member.edit(suppress=False)


@bot.command(name="close")
async def close():
    await bot.close()
    print("is ded")


@bot.command(name="nowplaying", description="Command to check what song is currently playing", aliases=['np'])
async def nowplaying(ctx):
    try:
        if not Vc.is_playing():
            await ctx.reply("I need to play something first")
    except:
        await ctx.reply("I need to play something first")
    else:
        audiofile = eyed3.load(f"songs/{Tune}")
        artist = audiofile.tag.artist
        title = audiofile.tag.title
        album = audiofile.tag.album
        embed = discord.Embed(color=0xc0f207)
        embed.set_author(name="Now Playing 🎶", icon_url=ctx.guild.icon_url)\
            .add_field(
            name="Playing", value=f"{title} - {artist}", inline=False)\
            .set_footer(text=f"Requested by {ctx.message.author} \t\nThis bot is still in development, if you have any queries, please contact the owner")
        if album is not None:
            embed.add_field(name="Album", value=f"{album}", inline=True)
            if albumart is not None:
                try:
                    embed.set_thumbnail(url=albumart[album])
                except KeyError:
                    print(albumart)
                    pass
        else:
            pass
        await ctx.reply(embed=embed)

bot.run(TOKEN, bot=True, reconnect=True)
