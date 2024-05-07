from textwrap import dedent

from langchain_core.prompts import ChatPromptTemplate

base_instructions = dedent(
    """\
                You are a helpful and friendly chatbot with peronality name Yumi.
                """
)
base_query = dedent(
    """\
        The Human says:{query}
        """
)

GENERAL_PROMPT = ChatPromptTemplate.from_messages(
    [("system", base_instructions), ("user", base_query)]
)
