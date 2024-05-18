from textwrap import dedent

import discord

from api_functions import get_weather
from config import Config, yumi_logger
from llm import baisc_conversation, basic_rag_conversation
from rag_pinecone import load_pdfs_to_pinecone

configs = Config()


class YumiClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
        yumi_logger.info("Logged in as %s (ID: %s)", self.user, self.user.id)

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
            yumi_logger.info("Uploading Attachments to Pinecone")
            response = await load_pdfs_to_pinecone(
                attachments=message.attachments, index_name="yumi-test-1"
            )  # Future: message.content

        elif message.content.startswith("!rag "):
            yumi_logger.debug("--> Starting RAG Conversation <--")
            async with message.channel.typing():
                response = await basic_rag_conversation(
                    query=message.content[5:],
                    config={"configurable": {"session_id": "abc123"}},
                )

        else:
            async with message.channel.typing():
                yumi_logger.debug("--> Starting Basic Conversation <--")
                response = await baisc_conversation().ainvoke(
                    {"query": message.content},
                    config={"configurable": {"session_id": "abc123"}},
                )

        # Send the response in chunks of 2000 characters due character limit
        i = 0
        for i in range(0, len(response), 2000):
            await message.channel.send(response[i : i + 2000])  # noqa: E203


intents = discord.Intents.default()
intents.message_content = True
intents.typing = True

client = YumiClient(intents=intents)
client.run(configs.BOT_TOKEN)
