import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Function to generate technical questions based on the input
def generate_questions_prompt(candidate_name, job_role):
    prompt = f"""
    I am a hiring assistant. I have a candidate named {candidate_name} applying for the position of {job_role}. 
    Please generate a list of 5 technical questions that would be appropriate for this job role.
    """
    return prompt

# Function to call Gemini API for content generation
def call_llm(prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")  # Choose your model
    response = model.generate_content(prompt)
    return response.text
