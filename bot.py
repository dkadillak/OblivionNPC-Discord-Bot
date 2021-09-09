import os
from discord import VoiceClient, utils, FFmpegPCMAudio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
FFMPEG_PATH = os.getenv('FFMPEG_PATH')

bot = commands.Bot(command_prefix='>')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='text')
async def written_quote(ctx):
    await ctx.send("Have you heard of the high elves?")


# https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg
@bot.command(alias=['speak', 'voice'])
async def play(ctx):
    audio_channel = ctx.author.voice.channel
    voice_client = audio_channel.connect
    audio_path = r'C:\Users\Devin Kadillak\Documents\dev_folder\Sound recordings\oblivion-guard\by-the-9-divines.mp3'
    audio_source = FFmpegPCMAudio(executable=FFMPEG_PATH, source=audio_path)
    if not voice_client.is_playing():
        voice_client.play(audio_source, after=lambda: voice_client.disconnect())


bot.run(TOKEN)

