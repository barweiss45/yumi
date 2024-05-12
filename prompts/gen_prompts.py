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
