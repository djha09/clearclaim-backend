import json
from read_pdf import read_pdf_file
from simplify import simplifyit

def simplify_policy_pdf(pdf_path):
    text = read_pdf_file(pdf_path)

    # Save the original text for rebuttal use
    with open("original_policy.json", "w") as f:
        json.dump({"text": text}, f, indent=2)

    simplified = simplifyit(text)

    return {
        # "original": text,
        "summary": simplified.strip()
    }
