import asyncio
import os
import dotenv
import discord
import logging
import requests
from io import BytesIO
from pydub import AudioSegment

dotenv.load_dotenv()

TOKEN = str(os.getenv("TOKEN"))
API_KEY = str(os.getenv("API_KEY"))

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

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
        return AudioSegment.from_file(BytesIO(response.content)).export("/tmp/john.mp3", format="mp3")


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
        await ctx.edit(content=shortened_text,file=discord.File(synthesize_voice(text)))
    except Exception as e:
        print(e)
        print("Something went wrong")

bot.run(TOKEN)
