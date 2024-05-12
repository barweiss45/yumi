import os
from textwrap import dedent
import logging

import discord
from dotenv import load_dotenv

from api_functions import get_weather
from llm import with_message_history

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
logger = logging.getLogger(__name__)


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

        elif message.attachments is not []:
            logger.debug(
                f"Received file: {[file.filename for file in message.attachments]}"
            )
            await message.channel.send(
                f"Received file: {[file.filename for file in message.attachments]}"
            )

        else:
            async with message.channel.typing():
                response = with_message_history.ainvoke(
                    {"query": message.content},
                    config={"configurable": {"session_id": "def234"}},
                )
                await message.channel.send(await response)


intents = discord.Intents.default()
intents.message_content = True
intents.typing = True

client = YumiClient(intents=intents)
client.run(BOT_TOKEN)
