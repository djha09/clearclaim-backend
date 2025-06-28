import os
import openai
from dotenv import load_dotenv

load_dotenv()
api = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(
    api_key=api,
    base_url="https://openrouter.ai/api/v1",
)

def ask_insurance_question(user_query, pdf_text=None):
    base = "You are a helpful insurance assistant."
    if pdf_text:
        base += f" Here is the user's insurance policy:\n{pdf_text}"
    base += f"\n\nQuestion: {user_query}"
    res =  client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": base}]
    )
    return res.choices[0].message["content"]
