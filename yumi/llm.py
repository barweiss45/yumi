import ell
import openai

from yumi.config import Config
from yumi.prompts.gen_prompts import base_instructions, basic_convo_prompt

configs = Config()


ell.init(verbose=True)


@ell.simple(model="gpt-4o-mini", client=openai.Client(api_key=configs.openai_api_key))
def baisc_conversation(query: str):
    """Basic conversation with GPT-4o-mini model."""
    return [
        ell.system(base_instructions),
        ell.system(basic_convo_prompt),
        ell.user(f"""{query}"""),
    ]
