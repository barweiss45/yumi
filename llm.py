from typing import Any, Dict

import tiktoken
from langchain.schema.output_parser import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
    RunnableSerializable,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI

from config import Config, yumi_logger
from prompts.gen_prompts import GENERAL_PROMPT, MEMORY_SUMMARIZATION_PROMPT, RAG_PROMPT
from rag_pinecone import basic_retriever

configs = Config()

google_api_key = configs.google_api_key
openai_api_key = configs.openai_api_key
mistralai_api_key = configs.mistralai_api_key

memory_store = {}

gemini_llm = ChatGoogleGenerativeAI(
    google_api_key=f"{google_api_key}",
    model="gemini-pro",
)  # Type: Ignore
mistral_llm = ChatMistralAI(model="mistral-large-latest")
openai_llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4o")


def summarize_memory(
    stored_session: InMemoryChatMessageHistory,
) -> InMemoryChatMessageHistory:
    summarization_chain = (MEMORY_SUMMARIZATION_PROMPT | gemini_llm).with_config(
        config={"run_name": "sumarize_memory"}
    )
    summary_message = summarization_chain.invoke({"history": stored_session.messages})
    stored_session.clear()
    stored_session.add_message(summary_message)
    yumi_logger.info("summarize_memory - Memory summarization complete.")
    return stored_session


def check_memory_token_size(messages: BaseChatMessageHistory) -> bool:
    yumi_logger.info("check_memory_token_size - Checking token size of memory.")
    encoding = tiktoken.get_encoding("cl100k_base")
    count = []
    for message in messages:
        token_count = len(encoding.encode(message.content))
        count.append(token_count)
    total_tokens = sum(count)
    if total_tokens > 500:
        yumi_logger.info(
            "check_memory_token_size - History token size exceeded: %s Tokens.",
            total_tokens,
        )
        return True
    else:
        yumi_logger.info(
            "check_memory_token_size - History token size: %s Tokens.", total_tokens
        )
        return False


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    Retrieve the chat message history for a given session ID.

    Args:
        session_id (str): The ID of the session.

    Returns:
        BaseChatMessageHistory: The chat message history for the session.

    """
    if session_id not in memory_store:
        yumi_logger.debug("get_session_history - Creating new session history.")
        memory_store[session_id] = ChatMessageHistory()
        return memory_store[session_id]
    stored_session: InMemoryChatMessageHistory = memory_store[session_id]
    if len(stored_session.messages) > 6:
        yumi_logger.debug(
            "get_session_history - stored_session exceeds 6 messages. \
                Checking Token Size..."
        )
        if check_memory_token_size(stored_session.messages):
            return summarize_memory(stored_session)
    return stored_session


def baisc_conversation() -> RunnableWithMessageHistory:
    basic_convo = GENERAL_PROMPT | openai_llm | StrOutputParser()
    with_message_history = RunnableWithMessageHistory(
        basic_convo,
        get_session_history,
        input_messages_key="query",
        history_messages_key="history",
    )
    return with_message_history


async def basic_rag_conversation(
    query: str, config: Dict[str, Dict[str, Any]]
) -> RunnableSerializable:
    basic_convo = RAG_PROMPT | openai_llm | StrOutputParser()
    with_message_history = RunnableWithMessageHistory(
        basic_convo,
        get_session_history,
        input_messages_key="query",
        history_messages_key="history",
    )
    retriever_runnable = RunnableLambda(basic_retriever)
    chain = (
        {"context": retriever_runnable, "query": RunnablePassthrough()}
        | with_message_history
        | StrOutputParser()
    )
    response = await chain.ainvoke(query, config)
    return response
