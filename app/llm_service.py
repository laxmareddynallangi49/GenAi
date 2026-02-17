from openai import OpenAI
from app.config import OPENAI_API_KEY, MODEL_NAME

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a document-restricted AI assistant.

Rules:
1. Answer ONLY using provided context.
2. Do NOT use outside knowledge.
3. If answer is not clearly in context, respond:
   "The answer is not available in the uploaded documents."
4. Do not guess.
"""

def generate_answer(context: str, question: str):

    if not context.strip():
        return "The answer is not available in the uploaded documents."

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Context:
{context}

Question:
{question}

Answer strictly from context.
"""
            }
        ]
    )

    return response.choices[0].message.content.strip()
