import os
import openai
from dotenv import load_dotenv

load_dotenv()
api = os.getenv("OPENAI_API_KEY")

if not api:
    raise ValueError("API_KEY not found in .env file")

client = openai.OpenAI(
    api_key=api,
    base_url="https://openrouter.ai/api/v1",
)

def simplifyit(text):
    prompt = f"""
Here is an insurance policy document:

\"\"\"{text}\"\"\"

Please explain it in short yet be clear and concise and simply for a person with no legal or insurance knowledge. 
Break it down like you're explaining it to a friend using plain English. You can also use situations to explain.
"""
    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful insurance explainer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error simplifying policy: {e}"
