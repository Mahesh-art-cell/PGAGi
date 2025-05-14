# import google.generativeai as genai
# import os

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # Use Gemini 1.5 Pro, the correct and available model
# model = genai.GenerativeModel('gemini-1.5-pro-latest')

# chat = model.start_chat(history=[])

# def get_gemini_response(prompt):
#     response = chat.send_message(prompt)
#     return response.text


import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=API_KEY)

# Function to call Gemini and get generated content
def call_llm(prompt):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")  # fast & free-tier friendly
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error from Gemini API: {str(e)}"

# Function to save candidate data to local JSON file
def save_candidate_data(data):
    os.makedirs("data", exist_ok=True)
    file_path = "data/candidates.json"

    # Load existing data
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            existing = json.load(f)
    else:
        existing = []

    # Add new entry
    existing.append(data)

    # Save back to file
    with open(file_path, "w") as f:
        json.dump(existing, f, indent=2)
