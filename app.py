import streamlit as st
import random

# Set up the page configuration
st.set_page_config(page_title="Interview Prep App", page_icon="💼", layout="wide")

st.title("💼 Job Interview Prep Hub")
st.write("Welcome to your personal interview preparation assistant! Use the sidebar to navigate through the tools.")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Interview Tips", "Question Bank", "Mock Interview"])

# --- PAGE 1: INTERVIEW TIPS ---
if page == "Interview Tips":
    st.header("💡 Top Interview Tips")
    st.markdown("""
    * **Research the Company:** Understand their mission, values, and recent news.
    * **The STAR Method:** Answer behavioral questions using **S**ituation, **T**ask, **A**ction, and **R**esult.
    * **Prepare Questions:** Always have 2-3 thoughtful questions ready to ask your interviewer at the end.
    * **Body Language:** Maintain good eye contact, sit up straight, and remember to smile!
    * **Follow Up:** Send a brief thank-you email within 24 hours of your interview.
    """)

# --- PAGE 2: QUESTION BANK ---
elif page == "Question Bank":
    st.header("📂 Common Interview Questions")
    
    st.subheader("Behavioral Questions")
    st.markdown("""
    1. Tell me about a time you overcame a significant challenge.
    2. Describe a situation where you had to work with a difficult team member.
    3. Can you tell me about a time you made a mistake and how you handled it?
    4. What is your greatest weakness, and how are you working to improve it?
    """)
    
    st.subheader("General Questions")
    st.markdown("""
    1. Walk me through your resume.
    2. Why are you interested in this role?
    3. Where do you see yourself in five years?
    """)

# --- PAGE 3: MOCK INTERVIEW ---
elif page == "Mock Interview":
    st.header("🎤 Mock Interview Practice")
    st.write("Click the button below to get a random interview question. Practice answering it out loud!")
    
    questions = [
        "Tell me about yourself.",
        "Why should we hire you over other candidates?",
        "Describe a time you failed and what you learned from it.",
        "Tell me about a time you showed leadership skills.",
        "How do you handle tight deadlines and pressure?",
        "What motivates you to do your best work?"
    ]
    
    if st.button("Generate Question"):
        random_question = random.choice(questions)
        st.success(f"**Question:** {random_question}")
        st.info("Take a moment to formulate your answer using the STAR method, then practice speaking it out loud.")
