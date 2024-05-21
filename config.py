import logging
import os

from dotenv import load_dotenv
from langchain_core.globals import set_debug

load_dotenv()
set_debug(True)

yumi_logger = logging.getLogger("Yumi")
# Set Discord root_looger to True will use Discord streammer
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# console_handler.setFormatter(formatter)
# yumi_logger.addHandler(console_handler)
yumi_logger.setLevel(logging.DEBUG)


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    mistralai_api_key = os.getenv("MISTRALAI_API_KEY")
