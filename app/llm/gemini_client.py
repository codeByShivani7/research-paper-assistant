import google.generativeai as genai

from app.core.config import settings

genai.configure(api_key=settings.gemini_api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_answer(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text