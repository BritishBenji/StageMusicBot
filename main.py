# StageMusicBot - https://discord.gg/qBq2WSsgvv
import asyncio
import json
import logging
from keep_alive import keep_alive
#PyNaCl#
import os
import random
import time
import discord
from discord.errors import ClientException
import eyed3
from discord import AudioSource, FFmpegPCMAudio, PCMVolumeTransformer, VoiceClient
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot
from discord.ext.commands.errors import CommandInvokeError
from discord_slash import SlashCommand, SlashContext



logging.basicConfig(level=logging.WARNING, filename="main.log", filemode="w")

guilds = []
directory = os.getcwd()



if os.path.exists("./albumart.json"):
    with open("./albumart.json", "r") as cjson:
        albumart = json.load(cjson)


def get_prefix(client, message):
    # sets the prefixes, you can keep it as an array of only 1 item if you need only one prefix
    prefixes = [os.getenv["prefix"]]

    if not message.guild:
        # Only allow set prefix as a prefix when in DMs, this is optional
        prefixes = [os.getenv["prefix"]]

    return commands.when_mentioned_or(*prefixes)(client, message)


bot = commands.Bot(
    command_prefix=get_prefix,
    description="A Music Bot to play Lindsey Stirling's amazing music, 24/7, just for you!",
    case_insensitive=True,
    help_command=None,
    intents=discord.Intents.all(),
)
slash = SlashCommand(bot, sync_commands=True)



@bot.event
async def on_ready():
    global save_guild
    if not os.path.exists("./songs"):
        logging.WARNING(
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
    stage = discord.utils.get(text_channel_list, name=(os.getenv["stage_name"]))
    channel = stage.name
    global Vc
    global Tune
    try:
        Vc = await stage.connect()
        member = guild.get_member(config["bot_id"])
        await member.edit(suppress=False)
    except CommandInvokeError:
        pass
    while True:
        while Vc.is_playing():
            await asyncio.sleep(1)
        else:
            Tune = get_info.write_song()
            Vc.play(discord.FFmpegPCMAudio(f"songs/{Tune}"))
            audiofile = eyed3.load(f"songs/{Tune}")
            title = audiofile.tag.title
            await bot.change_presence(activity=discord.Game(name=f"{title}"))
            Vc.source = discord.PCMVolumeTransformer(Vc.source, volume=config["volume"])
            if "suppress=False" in str(stage.voice_states):
                pass
            else:
                await member.edit(suppress=False)


@bot.command(name="close")
@commands.has_role(os.getenv("mod_role"))
async def close(ctx):
    logging.warning("Shutting down via command")
    logging.shutdown()
    await bot.close()


@slash.slash(
    name="nowplaying",
    description="Command to check what song is currently playing",
    guild_ids=(os.getenv("guilds_id")),
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
            icon_url=(ctx.author.avatar_url),
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

        await ctx.send(embed=embed)


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


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, ClientException):
        logging.warning(f"{error} - Bot closed due to disconnect")
        bot.close()
    if isinstance(error, UnicodeEncodeError):
        logging.warning(
            f"{error} - Bot has been muted whilst playing {Tune}, unmuting now"
        )
        await bot.edit(mute=False)





keep_alive()
bot.run(os.getenv("token"), bot=True, reconnect=True)
