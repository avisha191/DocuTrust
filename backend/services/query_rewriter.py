import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def rewrite_query(question):

    prompt = f"""
You are an Enterprise Retrieval-Augmented Generation (RAG) assistant.

A user has uploaded a document.

Rewrite the question ONLY to improve document retrieval.

Rules:
- Preserve the exact meaning.
- Keep the question about the uploaded document.
- Do NOT make it generic.
- Do NOT change the intent.
- Expand abbreviations only if useful.
- Return ONLY the rewritten question.

Question:
{question}

Rewritten Question:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()