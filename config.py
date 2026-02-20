# app/config.py

import os
import certifi
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API")
BASE_URL = os.getenv("BASE_URL")

#PERSIST_DIR = "./chroma_db"

FAISS_INDEX_PATH = "./faiss_index"


# SSL Fix
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
os.environ["TIKTOKEN_CACHE_DIR"] = "./token"