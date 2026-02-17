import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 3

MODEL_NAME = "gpt-4o-mini"

TTS_RATE = 180
TTS_VOLUME = 1.0
