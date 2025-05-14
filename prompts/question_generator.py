import os
from dotenv import load_dotenv
from prompts.fallback_questions import get_fallback_questions
import google.generativeai as genai

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def generate_questions(role):
    if not api_key:
        return get_fallback_questions(role)

    try:
        # Configure Gemini client
        genai.configure(api_key=api_key)

        # Use Gemini 1.5 Pro model
        model = genai.GenerativeModel("gemini-2.0-flash-lite")

        # Prompt
        prompt = f"Generate 5 short, clear, technical interview questions for the role: {role}."

        # Get response
        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return get_fallback_questions(role)