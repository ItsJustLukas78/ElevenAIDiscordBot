import os
import dotenv
import discord
import requests
from io import BytesIO
from pydub import AudioSegment

dotenv.load_dotenv()

TOKEN = str(os.getenv("TOKEN"))
API_KEY = str(os.getenv("API_KEY"))

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
    await ctx.send(file=discord.File(synthesize_voice(text)))


bot.run(TOKEN)
