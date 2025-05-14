
import streamlit as st
from dotenv import load_dotenv
import os
from prompts.generate_feedback import generate_feedback
from prompts.question_generator import generate_questions
from utils.conversation_flow import get_initial_prompt

# Load environment variables
load_dotenv()

# Streamlit config
st.set_page_config(
    page_title="TalentScout AI", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# App layout with columns for main content and right sidebar
col1, col2 = st.columns([3, 1])

with col1:
    # Title with icon and animation
    st.markdown("""
    <div class="title-container">
        <h1>🤖 TalentScout - AI InterviewBot</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Session state initialization
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.step = 0
        st.session_state.user_data = {}
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.current_q_index = 0
        st.session_state.feedback_rating = None  # For storing the feedback rating
        st.session_state.interview_complete = False
    
        initial_greeting = get_initial_prompt()
        st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

    # Display chat messages with enhanced styling
    for msg in st.session_state.messages:
        role_class = "message-bot" if msg["role"] == "assistant" else "message-user"
        st.markdown(f"<div class='{role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

    # Progress indicator during interview
    if st.session_state.step > 3 and not st.session_state.interview_complete:
        progress = min(1.0, (st.session_state.current_q_index + 1) / max(1, len(st.session_state.questions)))
        st.progress(progress)
        st.caption(f"Question {st.session_state.current_q_index + 1} of {len(st.session_state.questions)}")

# Chat logic
def get_bot_response(user_input):
    step = st.session_state.step
    user_data = st.session_state.user_data

    if step == 0:
        user_data["name"] = user_input
        st.session_state.step += 1
        return f"Nice to meet you, {user_input}! 👋 What's your email address?"

    elif step == 1:
        user_data["email"] = user_input
        st.session_state.step += 1
        return "Thanks! What's your phone number? 📱"

    elif step == 2:
        user_data["phone"] = user_input
        st.session_state.step += 1
        return "Great! What role are you looking for? 💼 (e.g., Python Developer, JavaScript Engineer, React Frontend Developer, etc.)"

    elif step == 3:
        user_data["role"] = user_input
        st.session_state.step += 1

        # Show loading message
        with st.spinner("Generating relevant interview questions..."):
            question_text = generate_questions(user_input)
            question_list = question_text.split("\n")
            st.session_state.questions = [q.strip("- ").strip() for q in question_list if q.strip()]
            st.session_state.current_q_index = 0

        if st.session_state.questions:
            return f"Let's begin your interview for *{user_input}* role. 🚀\n\n**Question 1:** {st.session_state.questions[0]}"
        else:
            return "Sorry, I couldn't find any questions for that role. Let's try something else."

    elif step == 4:
        st.session_state.answers.append(user_input)
        idx = st.session_state.current_q_index

        if idx < len(st.session_state.questions) - 1:
            st.session_state.current_q_index += 1
            return f"**Question {idx + 2}:** {st.session_state.questions[idx + 1]}"
        else:
            st.session_state.step += 1
            return "🎉 Thank you for completing all the questions! Enter 'generate feedback' to see your evaluation..."

    elif step == 5:
        # Generate feedback with loading indicator
        with st.spinner("Analyzing your responses..."):
            feedback = generate_feedback(
                st.session_state.questions,
                st.session_state.answers,
                st.session_state.user_data.get("role", "unknown role")
            )
        
        # Extract rating from feedback (simplified example)
        import re
        ratings = re.findall(r"Rating: (\d+)/10", feedback)
        if ratings:
            avg_rating = sum(int(r) for r in ratings) / len(ratings)
            rating_stars = "⭐" * int(round(avg_rating/2))
            st.session_state.feedback_rating = f"{rating_stars} {avg_rating:.1f}/10"
        else:
            st.session_state.feedback_rating = "⭐⭐⭐⭐ 8/10"
        
        st.session_state.step += 1
        st.session_state.interview_complete = True
        
        return f"""✅ **Interview Feedback**\n\n{feedback}\n\n**Overall Performance**: {st.session_state.feedback_rating}\n\nWould you like to start a new interview or discuss your results further?"""

    else:
        if "new interview" in user_input.lower() or "restart" in user_input.lower():
            # Reset session for new interview
            return "To start a new interview, please refresh the page."
        else:
            return "Feel free to ask any questions about your interview results or feedback. If you'd like to restart with a new interview, please refresh the page."

# Right sidebar for summary and feedback
with st.sidebar:
    st.markdown("### 📋 Interview Summary")
    user_data = st.session_state.user_data
    
    if "name" in user_data:
        st.markdown(f"👤 **Name:** {user_data['name']}")
    if "email" in user_data:
        st.markdown(f"📧 **Email:** {user_data['email']}")
    if "phone" in user_data:
        st.markdown(f"📱 **Phone:** {user_data['phone']}")
    if "role" in user_data:
        st.markdown(f"💼 **Role:** {user_data['role']}")

    if st.session_state.questions:
        st.markdown("---")
        st.markdown("### 🧠 Interview Q&A")
        
        # Add collapsible sections for Q&A
        for i, (q, a) in enumerate(zip(st.session_state.questions, st.session_state.answers)):
            with st.expander(f"Question {i+1}"):
                st.markdown(f"**Q:** {q}")
                st.markdown(f"*A:* {a}")
    
    if st.session_state.feedback_rating is not None:
        st.markdown("---")
        st.markdown("### 📊 Interview Rating")
        st.markdown(f"**Rating:** {st.session_state.feedback_rating}")
        
        # Add download button for interview report
        if st.session_state.interview_complete:
            # Create a simple report text
            report = f"""
            # TalentScout AI - Interview Report
            
            ## Candidate Information
            - **Name:** {user_data.get('name', 'N/A')}
            - **Email:** {user_data.get('email', 'N/A')}
            - **Phone:** {user_data.get('phone', 'N/A')}
            - **Role:** {user_data.get('role', 'N/A')}
            
            ## Interview Questions & Answers
            """
            
            for i, (q, a) in enumerate(zip(st.session_state.questions, st.session_state.answers)):
                report += f"\n### Question {i+1}\n**Q:** {q}\n**A:** {a}\n"
                
            report += f"\n## Overall Rating\n{st.session_state.feedback_rating}"
            
            st.download_button(
                label="📥 Download Interview Report",
                data=report,
                file_name=f"interview_report_{user_data.get('name', 'candidate')}.md",
                mime="text/markdown"
            )

# Handle user input
if prompt := st.chat_input("Your response..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Show typing indicator
    with st.spinner("Thinking..."):
        bot_response = get_bot_response(prompt)
        
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.rerun()


