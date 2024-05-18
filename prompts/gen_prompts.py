from textwrap import dedent

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

base_instructions = dedent(
    """\
    You are a helpful and friendly chatbot with peronality name Yumi.
    Your responses MUST be 2000 or fewer characters in length.
    """
)
base_query = dedent(
    """\
        The Human says:{query}
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
        (
            "user",
            """\
         Use the following pieces of retrieved context to answer the question.
         If you don't know the answer, just say that you don't know. Use three
         sentences maximum and keep the answer concise.
         Question: {query}
         Context: {context}
         """,
        ),
    ]
)
