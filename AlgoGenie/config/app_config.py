from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv
from config.constant import MODEL, GEMINI_MODEL_INFO

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_model_client():
    model_client = OpenAIChatCompletionClient(
        model=MODEL,
        api_key=GEMINI_API_KEY,
        model_info=GEMINI_MODEL_INFO
    )

    return model_client

