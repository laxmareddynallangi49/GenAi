# app/llm_service.py

import httpx
from langchain_openai import ChatOpenAI
from kuber.config import API_KEY, BASE_URL

client = httpx.Client(verify=False)

def get_llm():
    return ChatOpenAI(
        base_url=BASE_URL,
        model="azure_ai/genailab-maas-DeepSeek-V3-0324",
        api_key=API_KEY,
        http_client=client,
        temperature=0
    )