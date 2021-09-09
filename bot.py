from os import getenv
from asyncio import sleep
from math import ceil
from mutagen.mp3 import MP3
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
    audio_channel = ctx.author.voice.channel
    voice_client = await audio_channel.connect()

    wait_time = ceil(MP3(AUDIO_PATH).info.length)

    audio_source = FFmpegPCMAudio(source=AUDIO_PATH)

    # plays audio clip then leaves after the clip has ended by using length of clip (ceil) in seconds
    if not voice_client.is_playing():
        voice_client.play(audio_source)
        await sleep(wait_time)
        await voice_client.disconnect()


bot.run(TOKEN)

