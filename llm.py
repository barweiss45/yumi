import os
from typing import Any, Dict

from langchain.schema.output_parser import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough,
    RunnableSerializable,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI

from prompts.gen_prompts import GENERAL_PROMPT, RAG_PROMPT
from rag_pinecone import basic_retriever

google_api_key = os.getenv("GOOGLE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
mistralai_api_key = os.getenv("MISTRALAI_API_KEY")

memory_store = {}

gemini_llm = ChatGoogleGenerativeAI(
    google_api_key=f"{google_api_key}",
    model="gemini-pro",
)  # Type: Ignore
mistral_llm = ChatMistralAI(model="mistral-large-latest")
openai_llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4o")


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in memory_store:
        memory_store[session_id] = ChatMessageHistory()
    return memory_store[session_id]


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
