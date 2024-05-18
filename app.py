import logging
import os
from textwrap import dedent

import discord
from dotenv import load_dotenv

from api_functions import get_weather
from llm import baisc_conversation, basic_rag_conversation
from rag_pinecone import load_pdfs_to_pinecone

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

        elif len(message.attachments) > 0:
            logger.debug(
                f"Received file: {[file.filename for file in message.attachments]}"
            )
            pincone_response = await load_pdfs_to_pinecone(
                attachments=message.attachments, index_name="yumi-test-1"
            )  # Future: message.content
            await message.channel.send(pincone_response)

        elif message.content.startswith("!rag "):
            async with message.channel.typing():
                response = basic_rag_conversation(
                    query=message.content[5:],
                    config={"configurable": {"session_id": "abc123"}},
                )
                await message.channel.send(await response)

        else:
            async with message.channel.typing():
                response = baisc_conversation().ainvoke(
                    {"query": message.content},
                    config={"configurable": {"session_id": "def234"}},
                )
                await message.channel.send(await response)


intents = discord.Intents.default()
intents.message_content = True
intents.typing = True

client = YumiClient(intents=intents)
client.run(BOT_TOKEN)
