from textwrap import dedent

from langchain.prompts import ChatPromptTemplate


class BasicConvoPrompt(ChatPromptTemplate):
    def __init__(self):
        self.base_instructions = dedent(
            """\
    You are a helpful and friendly chatbot with peronality name Yumi."""
        )
        self.base_query = dedent(
            """\
                                 The Human says:{query}
                                 """
        )

    # @property
    # def prompt(self):
    #     chafrom_messages(
    #         [
    #             ("system", self.base_instructions),
    #             ("user", self.base_query)
    #             ]
    #             )
    #     return self._base_prompt
