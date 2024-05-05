import os
from textwrap import dedent

import discord
from dotenv import load_dotenv

from api_functions import get_weather
from llm import basic_convo

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


class YumiClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith("!chat"):
            query = message.content.split("!chat ")[1]
            response = basic_convo.ainvoke({"query": query})
            await message.channel.send(await response)

        if message.content.startswith("!weather"):
            city = message.content.split("!weather ")[1]
            weather_data = get_weather(city)
            weather_description = weather_data["weather"][0]["description"]
            temperature = weather_data["main"]["temp"]
            await message.channel.send(
                dedent(
                    f"""\
                    The weather in {city} is {weather_description} with
                    a temperature of {temperature:.2f}°C"""
                )
            )

        if message.content.startswith("!ping"):
            await message.channel.send("pong")
        else:
            response = basic_convo.ainvoke({"query": message.content})
            await message.channel.send(await response)


intents = discord.Intents.default()
intents.message_content = True

client = YumiClient(intents=intents)
client.run(BOT_TOKEN)
