import discord

from config import Config, yumi_logger
from llm import baisc_conversation, basic_rag_conversation, get_weather
from rag_pinecone import load_pdfs_to_pinecone

configs = Config()


class YumiClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
        yumi_logger.info("Logged in as %s (ID: %s)", self.user, self.user.id)

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
                llm_action = get_weather
            case _ if message.content.startswith("!rag "):
                llm_action = basic_rag_conversation
            case _:
                llm_action = baisc_conversation

        if llm_action is not None:
            async with message.channel.typing():
                response = await llm_action(
                    {"query": message.content},
                    config={"configurable": {"session_id": "abc123"}},
                )

        # Send the response in chunks of 2000 characters due character limit
        i = 0
        for i in range(0, len(response), 2000):
            return await message.channel.send(response[i : i + 2000])  # noqa: E203

        # elif message.content.startswith("!weather "):
        #     async with message.channel.typing():
        #         yumi_logger.debug("--> Starting Weather Conversation <--")
        #         response = await get_weather(
        #             query=message.content.split("!weather ")[1],
        #             config={"configurable": {"session_id": "abc123"}})

        # elif message.content.startswith("!rag "):
        #     yumi_logger.debug("--> Starting RAG Conversation <--")
        #     async with message.channel.typing():
        #         response = await basic_rag_conversation(
        #             query=message.content.split("!rag ")[1],
        #             config={"configurable": {"session_id": "abc123"}},
        #         )

        # elif len(message.attachments) > 0:
        #     yumi_logger.debug("--> Uploading Attachments to Pinecone <--")
        #     response = await load_pdfs_to_pinecone(
        #         attachments=message.attachments, index_name="yumi-test-1"
        #     )  # Future: message.content
        #     return await message.channel.send(response)

        # else:
        #     async with message.channel.typing():
        #         yumi_logger.debug("--> Starting Basic Conversation <--")
        #         response = await baisc_conversation().ainvoke(
        #             {"query": message.content},
        #             config={"configurable": {"session_id": "abc123"}},
        #         )

        # # Send the response in chunks of 2000 characters due character limit
        # i = 0
        # for i in range(0, len(response), 2000):
        #     await message.channel.send(response[i : i + 2000])  # noqa: E203


intents = discord.Intents.default()
intents.message_content = True
intents.typing = True

client = YumiClient(intents=intents)
client.run(configs.BOT_TOKEN)
