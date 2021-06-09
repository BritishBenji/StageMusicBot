# Radio Stirling Bot - https://discord.gg/lindseystirling
import asyncio
import json
import os
import random
import time

import discord
from discord.ext.commands.errors import CommandInvokeError
import eyed3
from discord import AudioSource, FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands
from discord.ext.commands.bot import Bot

guilds = []
directory = os.getcwd()


def get_prefix(client, message):
    # sets the prefixes, you can keep it as an array of only 1 item if you need only one prefix
    prefixes = ['£']

    if not message.guild:
        # Only allow '*' as a prefix when in DMs, this is optional
        prefixes = ['*']

    return commands.when_mentioned_or(*prefixes)(client, message)


bot = commands.Bot(command_prefix=get_prefix, description="A Music Bot to play Lindsey Stirling's amazing music, 24/7, just for you!",
                   case_insensitive=True, help_command=None)

# collect token here
with open(f"{directory}\\Token.txt", "r") as file1:
    TOKEN = file1.readlines()
TOKEN = " ".join(TOKEN)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    while len(guilds) < 1:
        async for guild in bot.fetch_guilds(limit=5):
            guilds.append(guild.name)
    print(guilds)


@bot.command(name="join", description="Command to make bot join channel")
@commands.has_role("Moderator")
async def join(ctx):
    stage = discord.utils.get(ctx.guild.channels, name="Radio Stirling")
    channel = stage.name
    global vc
    global tune
    try:
        vc = await stage.connect()
        self_user = bot.user
        member = await ctx.guild.fetch_member(self_user.id)
        await member.edit(suppress=False)
    except CommandInvokeError:
        pass
    played = []
    while True:
        while vc.is_playing():
            await asyncio.sleep(1)
        else:
            repeated = True
            while repeated:
                if len(played) > 20:
                    played = []
                tune = random.choice(os.listdir("songs/"))
                while tune in played:
                    tune = random.choice(os.listdir("songs/"))
                played.append(tune)
                repeated = False
            vc.play(discord.FFmpegPCMAudio(f'songs/{tune}'))
            audiofile = eyed3.load(f"songs/{tune}")
            title = audiofile.tag.title
            await bot.change_presence(
                activity=discord.Game(name=f"{title}"))
            vc.source = discord.PCMVolumeTransformer(vc.source, volume=0.2)
            if "suppress=False" in str(stage.voice_states):
                pass
            else:
                await member.edit(suppress=False)
            


@bot.command(name="close")
async def close(ctx):
    await bot.close()
    print("is ded")


@bot.command(name="nowplaying", description="Command to check what song is currently playing", aliases=['np'])
async def nowplaying(ctx):
    channels = [816534865343807488, 844729715477446687]
    if ctx.channel.id not in channels:
        return
    try:
        if not vc.is_playing():
            await ctx.send("I need to play something first")
    except:
        await ctx.send("I need to play something first")
    else:
        audiofile = eyed3.load(f"songs/{tune}")
        artist = audiofile.tag.artist
        title = audiofile.tag.title
        album = audiofile.tag.album
        embed = discord.Embed(color=0xc0f207)
        embed.set_author(name="Now Playing ♪", icon_url=ctx.guild.icon_url)
        embed.add_field(
            name="Playing", value=f"{title} - {artist}", inline=False)
        if album != None:
            embed.add_field(name="Album", value=f"{album}", inline=True)
        embed.set_footer(text=f"Requested by {ctx.message.author} \t\nThis bot is still in development, if you have any queries, please contact the owner")
        if album == "Artemis (Target Edition)":
            embed.set_thumbnail(
                url="https://img.discogs.com/cdYjdTx2FgdNZqtIKjrTG_gCNPw=/fit-in/600x526/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/R-14103238-1579259034-9722.jpeg.jpg")
        if album == "Lindsey Stirling":
            embed.set_thumbnail(
                url="https://img.discogs.com/mV563OeKH0SK_9oIoU1IdIEPPd4=/fit-in/600x600/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/R-3914178-1349900850-1613.jpeg.jpg")
        if album == "Brave Enough":
            embed.set_thumbnail(
                url="https://img.discogs.com/_UFoJ_k-W0JehnthOuq875r_7ek=/fit-in/600x600/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/R-8936283-1471815599-1562.jpeg.jpg")
        if album == "Warmer In The Winter (Deluxe Version)":
            embed.set_thumbnail(
                url="https://img.discogs.com/GSBuSi2FPtijB-89u3vqsY8IAgE=/fit-in/600x600/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/R-11052129-1537201543-1109.png.jpg")
        if album == "Shatter Me":
            embed.set_thumbnail(
                url="https://img.discogs.com/_3WLRJz00FgHM1bJXD_VIliftwk=/fit-in/600x586/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/R-5673193-1586641990-8024.jpeg.jpg")

        await ctx.send(embed=embed)

bot.run(TOKEN, bot=True, reconnect=True)
