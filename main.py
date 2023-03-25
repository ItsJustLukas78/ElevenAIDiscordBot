import os
import subprocess
from io import BytesIO

import discord
import dotenv
import requests
from discord.commands import Option, OptionChoice
from pydub import AudioSegment

dotenv.load_dotenv()

TOKEN = str(os.getenv("TOKEN"))
API_KEY = str(os.getenv("API_KEY"))

bot = discord.Bot()

valid_people = [
    OptionChoice(name="Atiksh"),  #  Value must be a string.
    OptionChoice(name="Jaiveer"),  #  Value must be a string.
    OptionChoice(name="Mohit"),  #  Value must be a string.
    OptionChoice(name="Jeia"),  #  Value must be a string.
]

people_id = {
    "Atiksh": "GFQHWEgWJSK1LDz2fIvd",
    "Jaiveer": "1ADc1J6ZDdBDU530Ui0l",
    "Mohit": "COFlDl1q31sQ94dpE77R",
    "Jeia": "PYtn8USM9TUL1bedV8Mo",
}


def synthesize_voice(text, person, stability, clarity_similarity_boost):
    url = "https://api.elevenlabs.io/v1/text-to-speech/" + people_id.get(person)
    headers = {"accept": "audio/mpeg", "xi-api-key": API_KEY}
    data = {
        "text": text,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": clarity_similarity_boost,
        },
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print("Error: " + str(response.status_code) + " getting voice")
        return None
    else:
        AudioSegment.from_file(BytesIO(response.content)).export(
            "/tmp/john.mp4", format="mp4"
        )
        subprocess.call(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "error",
                "-loop",
                "1",
                "-framerate",
                "1",
                "-i",
                f"{person}.jpg",
                "-i",
                "/tmp/john.mp4",
                "-map",
                "0:v",
                "-map",
                "1:a",
                "-r",
                "10",
                "-vf",
                "scale='iw-mod(iw,2)':'ih-mod(ih,2)', format=yuv420p",
                "-movflags",
                "+faststart",
                "-shortest",
                "-fflags",
                "+shortest",
                "-max_interleave_delta",
                "100M",
                "-af",
                "apad=pad_dur=1",
                "tmp_john.mp4",
            ]
        )
        return "tmp_john.mp4"


async def process_synth_request(ctx, text, person, stability, clarity_similarity_boost):
    shortened_text = text[:500] + "..."
    stability = stability
    clarity_similarity_boost = clarity_similarity_boost
    try:
        await ctx.respond("Synthesizing voice...")
        await ctx.edit(
            content=f"Stability: {str(stability)}\nClarity+Similarity: {str(clarity_similarity_boost)}\n{shortened_text}",
            file=discord.File(
                synthesize_voice(text, person, stability, clarity_similarity_boost)
            ),
        )
    except Exception as e:
        await ctx.edit(
            content="Sorry, your request could not be processed"
        )


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="atiksh", description="make atiksh speak")
async def atiksh(
    ctx,
    text: Option(str, "spoken text", required=True),
    stability: Option(
        float,
        "Make speech more expressive; can also lead to instabilities.",
        required=False,
        min_value=0.0,
        max_value=1.0,
        default=0.2,
    ),
    clarity_similarity_boost: Option(
        float,
        "Low values are recommended if background artifacts are present in "
        "generated speech.",
        required=False,
        min_value=0.0,
        max_value=1.0,
        default=0.3,
    ),
):
    await process_synth_request(
        ctx, text, "Atiksh", stability, clarity_similarity_boost
    )


@bot.slash_command(name="jaiveer", description="make jaiveer speak")
async def jaiveer(
    ctx,
    text: Option(str, "spoken text", required=True),
    stability: Option(
        float,
        "Make speech more expressive; can also lead to instabilities.",
        required=False,
        min_value=0.0,
        max_value=1.0,
        default=0.2,
    ),
    clarity_similarity_boost: Option(
        float,
        "Low values are recommended if background artifacts are present in "
        "generated speech.",
        required=False,
        min_value=0.0,
        max_value=1.0,
        default=0.3,
    ),
):
    await process_synth_request(
        ctx, text, "Jaiveer", stability, clarity_similarity_boost
    )


@bot.slash_command(name="mohit", description="make mohit speak")
async def mohit(
    ctx,
    text: Option(str, "spoken text", required=True),
    stability: Option(
        float,
        "Make speech more expressive; can also lead to instabilities.",
        required=False,
        min_value=0.0,
        max_value=1.0,
        default=0.2,
    ),
    clarity_similarity_boost: Option(
        float,
        "Low values are recommended if background artifacts are present in "
        "generated speech.",
        required=False,
        min_value=0.0,
        max_value=1.0,
        default=0.3,
    ),
):
    await process_synth_request(
        ctx, text, "Mohit", stability, clarity_similarity_boost
    )


@bot.slash_command(name="jeia", description="make jeia speak")
async def jeia(
    ctx,
    text: Option(str, "spoken text", required=True),
    stability: Option(
        float,
        "Make speech more expressive; can also lead to instabilities.",
        required=False,
        min_value=0.0,
        max_value=1.0,
        default=0.1,
    ),
    clarity_similarity_boost: Option(
        float,
        "Low values are recommended if background artifacts are present in "
        "generated speech.",
        required=False,
        min_value=0.0,
        max_value=1.0,
        default=1.0,
    ),
):
    await process_synth_request(
        ctx, text, "Jeia", stability, clarity_similarity_boost
    )


bot.run(TOKEN)
