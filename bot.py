import inspect
from os import getenv
from asyncio import sleep
from math import ceil
from mutagen.mp3 import MP3
from discord.ext.commands.errors import CommandInvokeError
from discord import VoiceClient, utils, FFmpegPCMAudio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')
FFMPEG_PATH = getenv('FFMPEG_PATH')
AUDIO_PATH = getenv('AUDIO_PATH')

bot = commands.Bot(command_prefix='>')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='text')
async def written_quote(ctx):
    await ctx.send("Have you heard of the high elves?")


@bot.command(name="speak")
async def play(ctx):

    # check if the caller is in a voice channel
    if ctx.author.voice is None:
        await ctx.reply("CITIZEN! you need to be in a voice channel first")

    else:

        cur_connections = 0

        if ctx.me.voice is not None:
            cur_connections = 1

        # check if we're already in a voice channel
        if cur_connections == 0:
            audio_channel = ctx.author.voice.channel

            voice_client = await audio_channel.connect()

            wait_time = ceil(MP3(AUDIO_PATH).info.length)

            audio_source = FFmpegPCMAudio(source=AUDIO_PATH)

            # plays audio clip then leaves after the clip has ended by using length of clip (ceil) in seconds
            if not voice_client.is_playing():
                voice_client.play(audio_source)
                await sleep(wait_time)
                await voice_client.disconnect()

        else:
            await ctx.reply("GAH! i'm currently in a voice channel. Try your command again in a moment citizen. ")


bot.run(TOKEN)

