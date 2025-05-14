# import os
# import json
# import streamlit as st
# import google.generativeai as genai

# # ✅ Use secrets (Streamlit Cloud method)
# API_KEY = st.secrets["GEMINI_API_KEY"]

# # Configure Gemini API
# genai.configure(api_key=API_KEY)

# # Function to call Gemini and get generated content
# def call_llm(prompt):
#     try:
#         model = genai.GenerativeModel(model_name="gemini-1.5-flash")  # fast & free-tier friendly
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         return f"❌ Error from Gemini API: {str(e)}"

# # Function to save candidate data to local JSON file
# def save_candidate_data(data):
#     os.makedirs("data", exist_ok=True)
#     file_path = "data/candidates.json"

#     # Load existing data
#     if os.path.exists(file_path):
#         with open(file_path, "r") as f:
#             existing = json.load(f)
#     else:
#         existing = []

#     # Add new entry
#     existing.append(data)

#     # Save back to file
#     with open(file_path, "w") as f:
#         json.dump(existing, f, indent=2)



import json
import os
import google.generativeai as genai

# Configure Gemini API with the key
def configure_genai(api_key):
    genai.configure(api_key=api_key)

# Function to call Gemini API for content generation
def call_llm(prompt):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")  # fast & free-tier friendly
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error from Gemini API: {str(e)}"

# Function to save candidate data to a local JSON file
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
