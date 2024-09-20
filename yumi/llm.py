import ell
import openai

from yumi.config import Config

configs = Config()


ell.init(verbose=True)


@ell.simple(model="gpt-4o-mini", client=openai.Client(api_key=configs.openai_api_key))
def baisc_conversation(query: str):
    """\
    You are a helpful and friendly chatbot 😀 with peronality name Yumi 👩‍🏫.
    You are here to help the user with any questions they may have. You
    have a sweet and friendly personality. You are confident and knowledgeable,
    you are modest and considerate.
    """  # System prompt
    return f"""\
    Use the following pieces of retrieved context to answer the question.
    If you don't know the answer, just say that you don't know. Keep the
    answer concise.

    Question: {query}
    """  # User prompt
