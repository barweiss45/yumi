# from typing import Any, Coroutine, Dict

# import tiktoken
# # from langchain.schema.output_parser import StrOutputParser
# # from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
# # from langchain_core.runnables import (
# #     Runnable,
# #     RunnableConfig,
# #     RunnableLambda,
# #     RunnablePassthrough,
# # )
# # from langchain_core.runnables.history import RunnableWithMessageHistory
# # from langchain_google_genai import ChatGoogleGenerativeAI
# # from langchain_mistralai import ChatMistralAI
# # from langchain_openai import ChatOpenAI

# from models.weather_api import WeatherLookup
# from prompts.gen_prompts import GENERAL_PROMPT, MEMORY_SUMMARIZATION_PROMPT, RAG_PROMPT
# from prompts.structured_output import (
#     GET_WEATHER_API_PROMPT,
#     GET_WEATHER_GENERATIVE_PROMPT,
# )
# from yumi.api_functions import get_current_weather
# from yumi.config import Config, yumi_logger
# from yumi.rag_pinecone import basic_retriever

# configs = Config()

# mistralai_api_key = configs.mistralai_api_key

# memory_store: Dict[str, ChatMessageHistory] = {}

# gemini_llm = ChatGoogleGenerativeAI(
#     model="gemini-pro",
# )
# mistral_llm = ChatMistralAI(model="mistral-large-latest")
# openai_llm: ChatOpenAI = ChatOpenAI(model="gpt-4o")


# def summarize_memory(
#     stored_session: ChatMessageHistory,
# ) -> ChatMessageHistory:
#     """
#     Summarizes the memory of a chat session.

#     Args:
#         stored_session (InMemoryChatMessageHistory): The chat session to be summarized.

#     Returns:
#         InMemoryChatMessageHistory: The chat session with the summary message added.
#     """
#     summarization_chain = (MEMORY_SUMMARIZATION_PROMPT | gemini_llm).with_config(
#         config={"run_name": "summarize_memory"}
#     )
#     summary_message = summarization_chain.invoke({"history": stored_session.messages})
#     stored_session.clear()
#     stored_session.add_message(summary_message)
#     yumi_logger.info("summarize_memory - Memory summarization complete.")
#     return stored_session


# def check_memory_token_size(messages: ChatMessageHistory) -> bool:
#     """
#     Check the token size of the memory.

#     Args:
#         messages (List[BaseMessage]): The chat message history.

#     Returns:
#         bool: True if the total token size exceeds 500, False otherwise.
#     """
#     yumi_logger.info("check_memory_token_size - Checking token size of memory.")
#     encoding = tiktoken.get_encoding("cl100k_base")
#     count = []
#     for message in messages:
#         token_count = len(encoding.encode(message.content))
#         count.append(token_count)
#     total_tokens = sum(count)
#     if total_tokens > 500:
#         yumi_logger.info(
#             "check_memory_token_size - History token size exceeded: %s Tokens.",
#             total_tokens,
#         )
#         return True
#     else:
#         yumi_logger.info(
#             "check_memory_token_size - History token size: %s Tokens.", total_tokens
#         )
#         return False


# def get_session_history(
#     session_id: str,
# ) -> Dict[str, ChatMessageHistory] | ChatMessageHistory:
#     """
#     Retrieve the chat message history for a given session ID.

#     Args:
#         session_id (str): The ID of the session.

#     Returns:
#         Dict[str, List[Basemessage]]: The chat message history for the session.

#     """
#     if session_id not in memory_store:
#         yumi_logger.debug("get_session_history - Creating new session history.")
#         memory_store[session_id] = ChatMessageHistory()
#         return memory_store[session_id]
#     stored_session: ChatMessageHistory = memory_store[session_id]
#     if len(stored_session.messages) > 6:
#         yumi_logger.debug(
#             "get_session_history - stored_session exceeds 6 messages. \
#                 Checking Token Size..."
#         )
#         if check_memory_token_size(stored_session.messages):
#             return summarize_memory(stored_session)
#     return stored_session


# async def baisc_conversation(
#     query: Dict[str, str], config: RunnableConfig
# ) -> Coroutine[Any, Any, Any]:
#     basic_convo: Runnable = GENERAL_PROMPT | openai_llm | StrOutputParser()
#     with_message_history = RunnableWithMessageHistory(
#         basic_convo,
#         get_session_history,
#         input_messages_key="query",
#         history_messages_key="history",
#     )
#     config["run_name"] = "basic_conversation"
#     response = await with_message_history.ainvoke(query, config)
#     return response


# async def basic_rag_conversation(query: Dict[str, str], config: RunnableConfig) -> str:
#     basic_convo: Runnable = RAG_PROMPT | openai_llm | StrOutputParser()
#     with_message_history = RunnableWithMessageHistory(
#         basic_convo,
#         get_session_history,
#         input_messages_key="query",
#         history_messages_key="history",
#     )
#     retriever_runnable = RunnableLambda(basic_retriever)
#     chain = (
#         {"context": retriever_runnable, "query": RunnablePassthrough()}
#         | with_message_history
#         | StrOutputParser()
#     )
#     config["run_name"] = "basic_rag_conversation"
#     response = await chain.ainvoke(query["query"], config)
#     return response


# async def get_weather(
#     query: Dict[str, str], config: RunnableConfig
# ) -> Coroutine[Any, Any, Any]:
#     """Retrieves the weather information for a given location."""

#     yumi_logger.info("get_weather - Getting weather information.")
#     get_location_chain: Runnable = {
#         "weather_api": (
#             GET_WEATHER_API_PROMPT | openai_llm.with_structured_output(WeatherLookup)
#         )
#     } | RunnableLambda(get_current_weather)

#     get_weather_generative = (
#         GET_WEATHER_GENERATIVE_PROMPT | openai_llm | StrOutputParser()
#     )

#     weather_chain: Runnable = {
#         "weather_api_response": get_location_chain,
#     } | get_weather_generative
#     yumi_logger.info("get_weather - Generating weather report.")

#     weather_chain_with_memory = RunnableWithMessageHistory(
#         weather_chain,
#         get_session_history,
#         input_messages_key="query",
#         history_messages_key="history",
#     )
#     config["run_name"] = "get_weather"
#     response = await weather_chain_with_memory.ainvoke(query, config)
#     return response


# if __name__ == "__main__":
#     raise NotImplementedError("This module is not meant to be executed directly.")
