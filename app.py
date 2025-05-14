# import streamlit as st
# from prompts import generate_questions_prompt  # if you use prompts
# from utils import call_llm, save_candidate_data

# st.set_page_config(page_title="Simple Digital Hiring Assistant", layout="centered")
# st.title("🤖 Digital Hiring Assistant")

# # Greeting
# st.markdown("""
# Welcome! I'm your assistant for initial screening. Please answer a few questions to begin.
# """)

# # Form to collect candidate info
# with st.form("candidate_form"):
#     name = st.text_input("Full Name")
#     email = st.text_input("Email")
#     education = st.text_input("Highest Qualification")
#     experience = st.slider("Years of Experience", 0, 20, 0)
#     role = st.selectbox("Preferred Role", ["Frontend Developer", "Backend Developer", "Full-Stack Developer", "Data Scientist"])
#     submitted = st.form_submit_button("Submit")

#     if submitted:
#         if not name or not email:
#             st.warning("Please fill in all required fields.")
#         else:
#             candidate_data = {
#                 "name": name,
#                 "email": email,
#                 "education": education,
#                 "experience": experience,
#                 "role": role
#             }

#             # Save candidate data
#             save_candidate_data(candidate_data)
#             st.success("✅ Candidate data saved successfully!")

#             # Optional: generate a confirmation message or questions
#             prompt = f"Generate 3 interview questions for a {role} with {experience} years of experience."
#             questions = call_llm(prompt)
#             st.subheader("🔍 Screening Questions")
#             st.write(questions)


import streamlit as st
import json
from prompts import generate_questions_prompt
from utils import call_llm, save_candidate_data

# Set page config
st.set_page_config(page_title="Digital Hiring Assistant", layout="centered")

# Apply custom CSS
st.markdown('<style>{}</style>'.format(open('style.css').read()), unsafe_allow_html=True)

# Title
st.title("🤖 Digital Hiring Assistant")

# Main container
with st.container():
    st.markdown("""
        Welcome! I'm your assistant for initial screening. Please answer a few questions to begin.
    """)

    # Form to collect candidate info
    with st.form("candidate_form"):
        st.markdown("### Candidate Information", unsafe_allow_html=True)
        
        # Candidate Information Inputs
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        job_role = st.selectbox("Job Role", ["Software Engineer", "Data Scientist", "Product Manager", "Other"])
        
        submit_button = st.form_submit_button("Submit")

        # Handle form submission
        if submit_button:
            # Generate questions
            prompt = generate_questions_prompt(name, job_role)
            questions = call_llm(prompt)
            
            # Save candidate data
            candidate_data = {
                "name": name,
                "email": email,
                "job_role": job_role
            }
            save_candidate_data(candidate_data)
            
            # Display the generated questions
            st.markdown("### Generated Questions for Interview:")
            st.write(questions)

            st.success("Your details have been successfully saved!")

# Exit button (outside the form)
exit_button = st.button("Exit", key="exit_button", use_container_width=True)
if exit_button:
    st.info("Thank you for your participation! You may now exit the assistant.")
    st.stop()  # Stop the app
