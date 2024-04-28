import os
from textwrap import dedent

from dotenv import load_dotenv
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
mistralai_api_key = os.getenv("MISTRALAI_API_KEY")

basic = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            dedent(
                """\
                You will take the role as a friendly and helpful chatbot named Yumi.
                Please answer the query"""
            ),
        ),
        ("human", "{query}"),
    ]
)

gemini_llm = ChatGoogleGenerativeAI(
    google_api_key=f"{google_api_key}",
    model="gemini-pro",
)  # Type: Ignore
mistral_llm = ChatMistralAI(model="mistral-large-latest")
openai_llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4")

basic_convo = basic | openai_llm | StrOutputParser()
