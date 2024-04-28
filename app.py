import os
from textwrap import dedent

import discord
from discord.ext import commands
from dotenv import load_dotenv

from api_functions import get_weather
from llm import basic_convo

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()

bot_description = """A Chatbot"""

bot = commands.Bot(command_prefix="!", description=bot_description, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.command()
async def chat(ctx, *, query: str):
    async with ctx.typing():
        response = basic_convo.ainvoke({"query": query})
        await ctx.send(await response)


@bot.command()
async def weather(ctx, city: str, units: str = "imperial"):
    weather_data = get_weather(city, units)
    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]
    await ctx.send(
        dedent(
            f"""\
                          The weather in {city} is {weather_description} with
                          a temperature of {temperature:.2f}°C"""
        )
    )


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


bot.run(token=str(BOT_TOKEN))
