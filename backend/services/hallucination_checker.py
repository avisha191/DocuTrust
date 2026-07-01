import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def check_hallucination(question, context, answer):

    prompt = f"""
You are a document verification system.

Your task is to verify whether the answer is completely supported by the provided document context.

Rules:
- Use ONLY the provided context.
- Ignore outside knowledge.
- If every important statement in the answer is supported by the context, reply YES.
- If any important statement is unsupported or invented, reply NO.
- Reply with ONLY YES or NO.

Context:
{context}

Question:
{question}

Answer:
{answer}
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

    result = response.choices[0].message.content.strip().upper()

    return result == "YES"