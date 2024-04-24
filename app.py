import os

from dotenv import load_dotenv
import discord
from discord.ext import commands

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
async def ping(ctx):
    await ctx.send("pong")


bot.run(BOT_TOKEN)
