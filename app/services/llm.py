import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL_NAME = "gemma-4-E4B-it"


if not API_KEY:
    raise ValueError("OPENAI_API_KEY is missing!")

if not BASE_URL:
    raise ValueError("OPENAI_BASE_URL is missing!")


client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)