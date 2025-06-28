from simplify import simplifyit
from read_pdf import read_pdf_file
import openai
import os
from dotenv import load_dotenv

load_dotenv()

api = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(
    api_key=api,
    base_url="https://openrouter.ai/api/v1",
)

def verify_from_pdf(pdf_text , claim):
    simplified = simplifyit(pdf_text)
    prompt = (
        "You are an insurance compliance assistant.\n\n"
        "Compare the following:\n\n"
        "Agent Explanation:\n"
        f"{claim}\n\n"
        "Policy Document:\n"
        f"{simplified}\n\n"
        "Your Task:\n"
        
        "- Identify if the agent explanation contains any misleading claims.\n"
        "- Point out any missing or contradictory information.\n"
        "- If the explanation is accurate and complete, state that clearly.\n"
        "Keep your response short, direct, and easy to understand."
        "Return your answer in **Markdown format** "
    )


    try:
        response = client.chat.completions.create(
            model = 'mistralai/mistral-7b-instruct',
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful and the best insurance expert."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        reply = response.choices[0].message.content.strip()
        return {'verify':reply}

    except Exception as e:
        return {"error" : f"OpenAI failed :{str(e)}"}
    
