import discord

from yumi.config import Config, yumi_logger
from yumi.llm import baisc_conversation
from yumi.rag_pinecone import load_pdfs_to_pinecone

configs = Config()


class YumiClient(discord.Client):
    """Yumi Discord Client Class"""

    async def on_ready(self):
        yumi_logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        yumi_logger.info("------")
        yumi_logger.info(f"Application Info: {await self.application_info()}")

    async def on_message(self, message):
        llm_action = None

        if message.author == self.user:
            return

        if len(message.attachments) > 0:
            yumi_logger.debug("--> Uploading Attachments to Pinecone <--")
            response = await load_pdfs_to_pinecone(
                attachments=message.attachments, index_name="yumi-test-1"
            )  # Future: message.content
            return await message.channel.send(response)

        match message.content:
            case _ if message.content.startswith("!weather "):
                # llm_action = get_weather
                pass
            # case _ if message.content.startswith("!rag "):
            #     llm_action = basic_rag_conversation
            case _:
                llm_action = baisc_conversation

        if llm_action is not None:
            async with message.channel.typing():
                response = llm_action(message.content)

        # Send the response in chunks of 2000 characters due character limit
        i = 0
        for i in range(0, len(response), 2000):
            return await message.channel.send(response[i : i + 2000])  # noqa: E203


intents = discord.Intents.default()
intents.message_content = True
intents.typing = True

client = YumiClient(intents=intents)
client.run(configs.BOT_TOKEN, root_logger=True)
