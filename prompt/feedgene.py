import os
from dotenv import load_dotenv
import google.generativeai as genai
from prompts.fallback_feedback import get_fallback_feedback  # You can define this as needed

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def generate_feedback(questions, answers, role):
    if not api_key:
        return get_fallback_feedback(questions, answers, role)

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-lite")

        # Create the prompt
        qa_pairs = "\n".join([f"Q{i+1}: {q}\nA{i+1}: {a}" for i, (q, a) in enumerate(zip(questions, answers))])
        prompt = f"""
You are an experienced technical interviewer. Analyze the following candidate's responses for the role of {role}.

For each question-answer pair:
1. Give a short feedback paragraph (1-3 lines) about the answer quality.
2. Provide a rating out of 10.
3. Mention areas of improvement, if any.

Here are the responses:
{qa_pairs}

Format your output like:
Q1 Feedback: ...
Rating: X/10
Improvement: ...

Q2 Feedback: ...
Rating: ...
Improvement: ...
"""

        # Generate content
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print("Error generating feedback:", e)
        return get_fallback_feedback(questions, answers, role)