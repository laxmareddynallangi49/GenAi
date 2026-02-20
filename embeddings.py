# app/embedding.py

import os
import httpx
import streamlit as st
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from kuber.config import API_KEY, BASE_URL, PERSIST_DIR

# client = httpx.Client(verify=False)

# def get_embedding_model():
#     return OpenAIEmbeddings(
#         base_url=BASE_URL,
#         model="azure/genailab-maas-text-embedding-3-large",
#         api_key=API_KEY,
#         http_client=client
#     )

# def load_vector_db():
#     if os.path.exists(PERSIST_DIR):
#         return Chroma(
#             persist_directory=PERSIST_DIR,
#             embedding_function=get_embedding_model()
#         )
#     return None

# def create_vector_db(chunks):
#     return Chroma.from_documents(
#         chunks,
#         get_embedding_model(),
#         persist_directory=PERSIST_DIR
#     )


# app/embedding.py
# app/embedding.py

# import os
# import httpx
# import pickle
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from kuber.config import API_KEY, BASE_URL
# from kuber.config import API_KEY, BASE_URL, FAISS_INDEX_PATH

# FAISS_INDEX_PATH = "faiss_index"

# # ------------------------------
# # 1️⃣ Optimized HTTP Client
# # ------------------------------
# client = httpx.Client(timeout=60.0,verify=False)

# _embedding_model = None
# _vector_db = None


# def get_embedding_model():
#     global _embedding_model

#     if _embedding_model is None:
#         _embedding_model = OpenAIEmbeddings(
#             base_url=BASE_URL,
#             model="azure/genailab-maas-text-embedding-3-large",
#             api_key=API_KEY,
#             http_client=client,
#             chunk_size=128  # batch embeddings
#         )

#     return _embedding_model


# # ------------------------------
# # 2️⃣ Load Existing FAISS Index
# # ------------------------------
# def load_vector_db():
#     global _vector_db

#     if os.path.exists(FAISS_INDEX_PATH):
#         _vector_db = FAISS.load_local(
#             FAISS_INDEX_PATH,
#             get_embedding_model(),
#             allow_dangerous_deserialization=True
#         )
#         return _vector_db

#     return None


# # ------------------------------
# # 3️⃣ Create or Append FAISS
# # ------------------------------
# def create_vector_db(chunks):
#     global _vector_db

#     embedding_model = get_embedding_model()

#     if os.path.exists(FAISS_INDEX_PATH):
#         _vector_db = FAISS.load_local(
#             FAISS_INDEX_PATH,
#             embedding_model,
#             allow_dangerous_deserialization=True
#         )

#         _vector_db.add_documents(chunks)

#     else:
#         _vector_db = FAISS.from_documents(
#             chunks,
#             embedding_model
#         )

#     _vector_db.save_local(FAISS_INDEX_PATH)
#     return _vector_db


import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import httpx

# -------------------------------
# CONFIG
# -------------------------------
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API")

client = httpx.Client(verify=False)

# -------------------------------
# Embedding Model
# -------------------------------
def get_embedding_model():
    return OpenAIEmbeddings(
        base_url=BASE_URL,
        model="azure/genailab-maas-text-embedding-3-large",
        api_key=API_KEY,
        http_client=client
    )


# -------------------------------
# Load Existing FAISS Vector DB
# -------------------------------
def load_vector_db(persist_dir="./faiss_db"):
    if os.path.exists(persist_dir):
        return FAISS.load_local(
            persist_dir,
            embedding=get_embedding_model()
        )
    return None


# -------------------------------
# Create New FAISS Vector DB
# -------------------------------
def create_vector_db(chunks, persist_dir="./faiss_db"):
    """
    chunks: List of Document objects
    """
    vector_db = FAISS.from_documents(
        chunks,
        embedding=get_embedding_model()
    )
    vector_db.save_local(persist_dir)
    return vector_db