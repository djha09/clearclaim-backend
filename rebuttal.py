from simplify import simplifyit
from read_pdf import read_pdf_file
import openai
import os
from dotenv import load_dotenv

load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure this env var is set

api = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(
    api_key=api,
    base_url="https://openrouter.ai/api/v1",
)

def generate_rebuttal_from_pdf(pdf_text, reason):
    simplified = simplifyit(pdf_text)
    prompt = f"""
    You are a professional insurance expert. Given the following insurance policy:

    {simplified}

    And the claim was denied for this reason:
    "{reason}"
    Your task is to write a direct , clear and firm Rebuttal that cites relevant policy terms and argues for reconsideration.
    The rebuttal argues why the denial was invalid and is up for reconsideration
    Keep your response short yet perfect as a rebuttal
    Return your response in **Markdown Format**
    """
    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct", messages=[
                {"role": "system", "content": "You are a helpful insurance expert."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return {"rebuttal": reply}  # Simple logic
    except Exception as e:
        return {"error": f"OpenAI failed: {str(e)}"}

def generate_rebuttal_from_text(reason):
    prompt = f"""
    You are an insurance expert. A user explained the following situation:
    "{reason}"
    
    Write a strong and professional rebuttal that challenges the denial with sound reasoning.
    """
    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct", messages=[
                {"role": "system", "content": "You are a professional claims advocate."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return {"rebuttal": reply, "matched_clauses": []}
    except Exception as e:
        return {"error": f"OpenAI error: {str(e)}"}





