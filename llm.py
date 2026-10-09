
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Check your .env file."
    )

client = Groq(api_key=GROQ_API_KEY)

MODEL_ID = "openai/gpt-oss-120b"

def generate_response(prompt: str) -> str:
    """Generate a response using the Groq API."""

    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            max_tokens=500,
            temperature=0.4,
        )

        answer = response.choices[0].message.content

        return answer or "The model returned an empty response."

    except Exception as exc:
        raise RuntimeError(
            f"Groq request failed: {exc}"
        ) from exc