import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_answer(question, context):

    prompt = f"""
You are DocuTrust, an enterprise document intelligence assistant.

Instructions:
- Answer using only the provided context.
- Format answers professionally.
- Use bullet points whenever possible.
- Do not say 'Based on the provided context'.
- Do not explain your reasoning.
- Extract the answer directly.
- If the context is partially relevant, provide the best answer possible from the available information.

Context:
{context}

Question:
{question}

Answer:
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

    return response.choices[0].message.content