import os

from dotenv import load_dotenv
from langchain.schema.output_parser import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI

from prompts.gen_prompts import BasicConvoPrompt

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
mistralai_api_key = os.getenv("MISTRALAI_API_KEY")

basic = BasicConvoPrompt()

gemini_llm = ChatGoogleGenerativeAI(
    google_api_key=f"{google_api_key}",
    model="gemini-pro",
)  # Type: Ignore
mistral_llm = ChatMistralAI(model="mistral-large-latest")
openai_llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4")

basic_convo = basic.prompt | openai_llm | StrOutputParser()
