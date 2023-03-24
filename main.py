import asyncio
import os
import subprocess
import dotenv
import discord
import logging
import requests
from io import BytesIO
from pydub import AudioSegment

dotenv.load_dotnv()

TOKEN = str(os.getenv("TOKEN"))
API_KEY = str(os.getenv("API_KEY"))

# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='/discord.log', encoding='utf-8', mode='a')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

bot = discord.Bot()


def synthesize_voice(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/GFQHWEgWJSK1LDz2fIvd"
    headers = {"accept": "audio/mpeg", "xi-api-key": API_KEY}
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.2,
            "similarity_boost": 0.3,
        }
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print("Error: " + str(response.status_code) + " getting voice")
        return None
    else:
        AudioSegment.from_file(BytesIO(response.content)).export("/tmp/john.mp4", format="mp4")
        subprocess.call(
            ['ffmpeg', '-loop', '1', '-framerate', '1', '-i', 'rizz.jpg', '-i', '/tmp/john.mp4', '-map', '0:v', '-map', '1:a', '-r', '10', '-vf', "scale='iw-mod(iw,2)':'ih-mod(ih,2)',format=yuv420p", '-movflags', '+faststart', '-shortest', '-fflags', '+shortest', '-max_interleave_delta', '100M', 'tmp_john.mp4'])
        return "tmp_john.mp4"


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="john", description="jitty johns")
async def hello(ctx):
    await ctx.respond("LETS GET THIS JOHN! JIT JITTY JIT JI")


@bot.slash_command(name="atiksh", description="make atiksh say some johns")
async def atiksh(ctx, text):
    shortened_text = text[:75] + "..."
    try:
        await ctx.respond("Synthesizing voice...")
        await ctx.edit(content=shortened_text, file=discord.File(synthesize_voice(text)))
    except Exception as e:
        print(e)
        print("Something went wrong")

bot.run(TOKEN)
