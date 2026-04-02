import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_polish_prompt(letter_type: str, details: str) -> str:
    return f"""
You are helping draft a Swiss tenancy-related letter.

Task:
Rewrite the user's case details into one concise, formal paragraph in French.

Rules:
- Use only the facts provided by the user.
- Do not invent facts.
- Do not cite legal articles.
- Do not give legal conclusions.
- Keep the tone formal and natural.
- Output only the paragraph text.

Letter type: {letter_type}

User details:
{details}
""".strip()

def polish_details(letter_type: str, details: str) -> str:
    if not details or not details.strip():
        return ""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=build_polish_prompt(letter_type, details),
    )
    return response.output_text.strip()