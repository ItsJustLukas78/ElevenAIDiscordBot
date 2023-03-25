import asyncio
import os
import subprocess
import dotenv
import discord
from discord.commands import Option, OptionChoice
import logging
import requests
from io import BytesIO
from pydub import AudioSegment

dotenv.load_dotenv()

TOKEN = str(os.getenv("TOKEN"))
API_KEY = str(os.getenv("API_KEY"))
CONSTANT_VOICE_ID = "GFQHWEgWJSK1LDz2fIvd"

bot = discord.Bot()

valid_people = [
    OptionChoice(name="Atiksh"), #  Value must be a string.
    OptionChoice(name="Jaiveer"), #  Value must be a string.
    OptionChoice(name="Mohit") #  Value must be a string.
]

people_id = {
    "Atiksh": "GFQHWEgWJSK1LDz2fIvd",
    "Jaiveer": "1ADc1J6ZDdBDU530Ui0l",
    "Mohit": "COFlDl1q31sQ94dpE77R"
}

def synthesize_voice(text, person, stability, clarity_similarity_boost):
    url = "https://api.elevenlabs.io/v1/text-to-speech/" + people_id.get(person, "GFQHWEgWJSK1LDz2fIvd")
    headers = {"accept": "audio/mpeg", "xi-api-key": API_KEY}
    data = {
        "text": text,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": clarity_similarity_boost,
        }
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print("Error: " + str(response.status_code) + " getting voice")
        return None
    else:
        AudioSegment.from_file(BytesIO(response.content)).export("/tmp/john.mp4", format="mp4")
        subprocess.call(
            ['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-framerate', '1', '-i', f'{person}.jpg', '-i', '/tmp/john.mp4', '-map', '0:v', '-map', '1:a', '-r', '10', '-vf', "scale='iw-mod(iw,2)':'ih-mod(ih,2)',format=yuv420p", '-movflags', '+faststart', '-shortest', '-fflags', '+shortest', '-max_interleave_delta', '100M', 'tmp_john.mp4'])
        return "tmp_john.mp4"


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="john", description="jitty johns")
async def hello(ctx):
    await ctx.respond("LETS GET THIS JOHN! JIT JITTY JIT JI")


@bot.slash_command(name="atiksh", description="make atiksh or jaiveer say some johns")
async def atiksh(
        ctx,
        text: Option(str, "spoken text", required=True),
        person: Option(str, "who is speaking", required=False, default=CONSTANT_VOICE_ID, choices=valid_people),
        stability: Option(float, "Make speech more expressive; can also lead to instabilities.", required=False, default=0.2),
        clarity_similarity_boost: Option(float, "Low values are recommended if background artifacts are present in "
                                                "generated speech.", required=False, default=0.3)
):
    shortened_text = text[:500] + "..."
    stability = stability if stability <= 1.0 else 0.2
    clarity_similarity_boost = clarity_similarity_boost if clarity_similarity_boost <= 1.0 else 0.3
    try:
        await ctx.respond("Synthesizing voice...")
        await ctx.edit(content=f"Stability: {str(stability)}\nClarity+Similarity: {str(clarity_similarity_boost)}\n{shortened_text}",
                       file=discord.File(synthesize_voice(text, person, stability, clarity_similarity_boost)))
    except Exception as e:
        print(e)
        print("Something went wrong")

bot.run(TOKEN)
