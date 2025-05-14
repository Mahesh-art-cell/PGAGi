
# import streamlit as st
# import json
# from prompts import generate_questions_prompt
# from utils import call_llm, save_candidate_data

# # Set page config
# st.set_page_config(page_title="Digital Hiring Assistant", layout="centered")

# # Apply custom CSS
# st.markdown('<style>{}</style>'.format(open('style.css').read()), unsafe_allow_html=True)

# # Title
# st.title("🤖 Digital Hiring Assistant")

# # Main container
# with st.container():
#     st.markdown("""
#         Welcome! I'm your assistant for initial screening. Please answer a few questions to begin.
#     """)

#     # Form to collect candidate info
#     with st.form("candidate_form"):
#         st.markdown("### Candidate Information", unsafe_allow_html=True)
        
#         # Candidate Information Inputs
#         name = st.text_input("Full Name")
#         email = st.text_input("Email Address")
#         job_role = st.selectbox("Job Role", ["Software Engineer", "Data Scientist", "Product Manager", "Other"])
        
#         submit_button = st.form_submit_button("Submit")

#         # Handle form submission
#         if submit_button:
#             # Generate questions
#             prompt = generate_questions_prompt(name, job_role)
#             questions = call_llm(prompt)
            
#             # Save candidate data
#             candidate_data = {
#                 "name": name,
#                 "email": email,
#                 "job_role": job_role
#             }
#             save_candidate_data(candidate_data)
            
#             # Display the generated questions
#             st.markdown("### Generated Questions for Interview:")
#             st.write(questions)

#             st.success("Your details have been successfully saved!")

# # Exit button (outside the form)
# exit_button = st.button("Exit", key="exit_button", use_container_width=True)
# if exit_button:
#     st.info("Thank you for your participation! You may now exit the assistant.")
#     st.stop()  # Stop the app


import os

import streamlit as st
import json
import google.generativeai as genai

# Load API key from Streamlit secrets
API_KEY = st.secrets["GEMINI_API_KEY"]

# Configure Gemini API with the key
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

# Streamlit UI for user input
st.set_page_config(page_title="Digital Hiring Assistant", layout="centered")
st.markdown('<style>{}</style>'.format(open('style.css').read()), unsafe_allow_html=True)

st.title("🤖 Digital Hiring Assistant")

# Main container
with st.container():
    st.markdown("""
        Welcome! I'm your assistant for initial screening. Please answer a few questions to begin.
    """)

    # Form to collect candidate info
    with st.form("candidate_form"):
        st.markdown("### Candidate Information", unsafe_allow_html=True)
        
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        job_role = st.selectbox("Job Role", ["Software Engineer", "Data Scientist", "Product Manager", "Other"])
        
        submit_button = st.form_submit_button("Submit")

        # Handle form submission
        if submit_button:
            prompt = generate_questions_prompt(name, job_role)
            questions = call_llm(prompt)
            
            # Save candidate data
            candidate_data = {
                "name": name,
                "email": email,
                "job_role": job_role
            }
            save_candidate_data(candidate_data)
            
            # Display generated questions
            st.markdown("### Generated Questions for Interview:")
            st.write(questions)

            st.success("Your details have been successfully saved!")

# Exit button
exit_button = st.button("Exit", key="exit_button", use_container_width=True)
if exit_button:
    st.info("Thank you for your participation! You may now exit the assistant.")
    st.stop()  # Stop the app
