from textwrap import dedent

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from yumi.util import get_current_time

base_instructions = dedent(
    """\
    You are a helpful and friendly chatbot 😀 with peronality name Yumi 👩‍🏫.
    You are here to help the user with any questions they may have. You
    have a sweet and friendly personality. You are confident and knowledgeable,
    you are modest and considerate.
    """
)
base_query = """{query}"""
base_rag_query = dedent(
    """\
        Use the following pieces of retrieved context to answer the question.
        If you don't know the answer, just say that you don't know. Keep the
        answer concise.
        Question: {query}
        Context: {context}
        """
)

summarize_memory = dedent(
    f"""\
                The mesages above are from an AI/Human chat session.
                You need to distill the above chat messages into a single
                summary message. Include as many specific details as you can.
                But be sure that it is done in a way that is concise and easy
                to understand as it will be used to summarize the chat history
                and used as reference later by the AI. Please also that this
                request was made on {get_current_time()}.
                """
)

GENERAL_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", base_instructions),
        MessagesPlaceholder(variable_name="history"),
        ("user", base_query),
    ]
)

RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", base_instructions),
        MessagesPlaceholder(variable_name="history"),
        ("user", base_rag_query),
    ]
)

MEMORY_SUMMARIZATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        (
            "user",
            summarize_memory,
        ),
    ]
)
