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

        elif message.content.startswith("!weather"):
            async with message.channel.typing():
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

        else:
            async with message.channel.typing():
                response = basic_convo.ainvoke({"query": message.content})
                await message.channel.send(await response)


intents = discord.Intents.default()
intents.message_content = True
intents.typing = True

client = YumiClient(intents=intents)
client.run(BOT_TOKEN)
