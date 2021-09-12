from os import getenv
from asyncio import sleep
from math import ceil
from mutagen.mp3 import MP3
from discord import Embed, FFmpegPCMAudio
from discord.ext import commands
from dotenv import load_dotenv
from random import randrange

from Mp3Indexer import index_mp3_files


load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')
FFMPEG_PATH = getenv('FFMPEG_PATH')

mp3_ind_short, mp3_ind_long = index_mp3_files()

bot = commands.Bot(command_prefix='>', help_command=None)
bot.remove_command('help')


def generate_speak_help() -> str:
    '''
    function generates the help message for the >speak command
    :return: string with the details of how to use the command
    '''
    no_arg = "\n>speak  =  random voice line\n"
    numbered_args = "\n".join([f'>speak {key}   =  {value}' for key, value in mp3_ind_short.items()])
    return f'{numbered_args}{no_arg}'


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='text', help="for testing if the bot is running")
async def written_quote(ctx):
    await ctx.send("Have you heard of the high elves?")


@bot.command(name="speak", help=generate_speak_help())
async def play(ctx, index: int = -1):

    # make sure caller gave me a valid index for the desired voiceline
    if index not in mp3_ind_long.keys() and index != -1:
        await ctx.reply("GAH! give me a number in the range of acceptable voice lines. use ``>help`` for more info")
    else:
        # check if the caller is in a voice channel
        if ctx.author.voice is None:
            await ctx.reply("CITIZEN! you need to be in a voice channel first")

        else:
            # using -1 as placeholder value for random voice line
            if index == -1:
                index = randrange(1, len(mp3_ind_short)+1)

            cur_connections = 0

            if ctx.me.voice is not None:
                cur_connections = 1

            # check if we're already in a voice channel
            if cur_connections == 0:
                audio_channel = ctx.author.voice.channel

                voice_client = await audio_channel.connect()

                wait_time = ceil(MP3(mp3_ind_long[index]).info.length)

                audio_source = FFmpegPCMAudio(source=mp3_ind_long[index])

                # plays audio clip then leaves after the clip has ended by using length of clip (ceil) in seconds
                if not voice_client.is_playing():
                    voice_client.play(audio_source)
                    await sleep(wait_time)
                    await voice_client.disconnect()

            else:
                # bot is already in a voice channel playing a voice line
                await ctx.reply("GAH! i'm currently in a voice channel. Try your command again in a moment citizen. ")


@bot.command(name="help", help="gives you more information about each command")
async def help(ctx, args=None):
    help_embed = Embed(title="Oblivion NPC")
    command_names_list = [x.name for x in bot.commands]

    # If there are no arguments, just list the commands:
    if not args:
        help_embed.add_field(
            name="List of supported commands:",
            value="\n".join(['>'+x.name for x in bot.commands]),
            inline=False
        )
        help_embed.add_field(
            name="Details",
            value="Each command starts with '>'\nType `>help -command name-` for more details about each command.",
            inline=False
        )

    # If the argument is a command, get the help text from that command:
    elif args in command_names_list:
        help_embed.add_field(
            name=args,
            value=bot.get_command(args).help
        )

    # If someone is just trolling:
    else:
        help_embed.add_field(
            name="Nope.",
            value="Don't think I got that command, boss!"
        )

    await ctx.send(embed=help_embed)


bot.run(TOKEN)

