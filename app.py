import streamlit as st
import pandas as pd
import numpy as np
import time
import random

# ==========================================
# 1. ENTERPRISE CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="Nexus AI - Enterprise Interview Prep",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Glassmorphism UI Injection
st.markdown("""
    <style>
    /* Global Styles */
    .main { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); color: #f8fafc; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; font-weight: 700; letter-spacing: -0.02em; }
    
    /* Glassmorphic Cards */
    .kpi-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Status Badges */
    .badge-premium {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session States for AI Flow
if "messages" not in st.session_state:
    st.session_state.messages = []
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False
if "current_question_idx" not in st.session_state:
    st.session_state.current_question_idx = 0

# ==========================================
# 2. SIDEBAR NAVIGATION & USER PROFILE
# ==========================================
with st.sidebar:
    st.markdown("<div style='text-align: center; padding: 20px 0;'><h2 style='color:#6366f1; margin:0;'>NEXUS AI</h2><p style='color:#94a3b8; font-size:12px;'>ENTERPRISE SUITE v2.0</p></div>", unsafe_allow_html=True)
    
    # Profile Completion Widget
    st.markdown("### 👤 Candidate Profile")
    st.caption("Profile Completion: 85%")
    st.progress(0.85)
    
    st.text_input("Target Role", value="Senior Full Stack Engineer")
    st.text_input("Target Company", value="Google / Stripe")
    
    st.markdown("---")
    menu = st.radio(
        "Navigation Matrix",
        ["📊 Executive Dashboard", "📝 ATS Resume Analyzer", "🤖 AI Mock Interview", "📚 Universal Question Bank", "💬 AI Career Assistant"]
    )
    
    st.markdown("---")
    st.markdown("<span class='badge-premium'>✨ PREMIUM ACCESS ACTIVATED</span>", unsafe_allow_html=True)

# ==========================================
# MODULE 1: EXECUTIVE DASHBOARD
# ==========================================
if menu == "📊 Executive Dashboard":
    st.title("Welcome Back, Executive Leader")
    st.subheader("Real-time Interview Readiness Analytics")
    
    # Row 1: Primary Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class='kpi-card'><h5>Readiness Score</h5><h2>84.2%</h2><span style='color:#10b981;'>↑ 3.4% this week</span></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='kpi-card'><h5>Resume ATS Score</h5><h2>78 / 100</h2><span style='color:#ef4444;'>↓ 2 points structural</span></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class='kpi-card'><h5>Coding Accuracy</h5><h2>91.5%</h2><span style='color:#10b981;'>↑ 1.2% optimization</span></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class='kpi-card'><h5>Daily Streak</h5><h2>14 Days 🔥</h2><span style='color:#6366f1;'>Top 5% of Candidates</span></div>""", unsafe_allow_html=True)
        
    st.markdown("### Performance Vector Analytics")
    
    # Analytical Chart Data Simulation
    chart_col1, chart_col2 = st.columns([2, 1])
    with chart_col1:
        st.write("#### Weekly Competency Development")
        chart_data = pd.DataFrame(
            np.random.randn(20, 3) + [5, 6, 7],
            columns=['Technical Architecture', 'System Design', 'Behavioral Leadership']
        )
        st.line_chart(chart_data)
    with chart_col2:
        st.write("#### Core Skill Allocation")
        skills_df = pd.DataFrame({
            "Skill Dimension": ["System Design", "Algorithms", "React/Next.js", "AI Integration", "Communication"],
            "Proficiency %": [85, 90, 78, 92, 88]
        })
        st.dataframe(skills_df, hide_index=True, use_container_width=True)

# ==========================================
# MODULE 2: ATS RESUME ANALYZER
# ==========================================
elif menu == "📝 ATS Resume Analyzer":
    st.title("Deep-Scan ATS Parsing Engine")
    st.write("Upload your production resume to evaluate against target enterprise parsing systems.")
    
    uploaded_file = st.file_uploader("Drop Resume PDF or DOCX", type=["pdf", "docx"])
    target_jd = st.text_area("Target Job Description (Paste Text Here)")
    
    if st.button("Execute Vector Match Optimization") and uploaded_file and target_jd:
        with st.spinner("Processing deep embeddings & text parsing..."):
            time.sleep(2.5) # Simulate heavy AI calculation
            
            st.success("Analysis Complete! Optimization Vector Generated Below.")
            
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric("ATS Structural Compatibility", "89%", delta="Highly Compatible")
                st.markdown("#### 🚨 Found Structural Red Flags")
                st.error("Missing Keyword Vectors: **Distributed Systems**, **Kubernetes Orchestration**, **GraphQL**")
            with res_col2:
                st.markdown("#### 🛠️ Suggested Bullet-Point Transformations")
                st.info("**Before:** Built an internal portal using Next.js and Tailwind.")
                st.success("**After (AI Optimized):** Engineered an enterprise-grade micro-frontend portal leveraging Next.js and tailwind CSS, increasing team velocity by 34% and reducing load times by 1.2s.")

# ==========================================
# MODULE 3: AI MOCK INTERVIEW
# ==========================================
elif menu == "🤖 AI Mock Interview":
    st.title("Simulated AI Interview Matrix")
    
    if not st.session_state.interview_started:
        st.write("Configure your highly targeted simulation instance below:")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            company = st.selectbox("Company Profile", ["Google", "Apple", "Netflix", "Stripe", "Custom Enterprise"])
        with col_b:
            role_type = st.selectbox("Interview Stack", ["System Design", "Technical Architecture", "Behavioral (STAR Method)", "HR & Leadership"])
        with col_c:
            difficulty = st.select_slider("Assessment Strictness", options=["Intern", "L4/Mid-Level", "L6/Senior Staff", "Principal Principal"])
            
        if st.button("Initialize Interview Loop"):
            st.session_state.interview_started = True
            st.session_state.interview_questions = [
                f"Welcome to your {company} {role_type} assessment. Let's start: How do you optimize database bottlenecks for an application processing 50k requests per second?",
                "Can you walk me through an architecture decision you made that ultimately failed, and how you recovered?",
                "How do you handle disagreement with a Principal Product Manager regarding core engineering trade-offs?"
            ]
            st.rerun()
            
    else:
        idx = st.session_state.current_question_idx
        questions = st.session_state.interview_questions
        
        if idx < len(questions):
            st.markdown(f"<div class='kpi-card' style='border-left: 5px solid #6366f1;'><h4>Interviewer Prompt {idx + 1} of {len(questions)}</h4><h3>{questions[idx]}</h3></div>", unsafe_allow_html=True)
            
            user_response = st.text_area("Type your technical response block here:", height=150, key=f"resp_{idx}")
            
            c1, c2 = st.columns([1, 5])
            with c1:
                if st.button("Submit Answer"):
                    with st.spinner("AI Evaluating Metrics..."):
                        time.sleep(1.5)
                        st.session_state.current_question_idx += 1
                        st.rerun()
            with c2:
                st.caption("Tip: Use the STAR method (Situation, Task, Action, Result) for engineering leadership questions.")
        else:
            st.success("🎉 Simulation Loop Concluded Successfully!")
            st.markdown("### Performance Feedback Matrices")
            
            f1, f2, f3 = st.columns(3)
            f1.metric("Technical Score", "92/100", "+4% Architecture")
            f2.metric("Communication / Clarity", "85/100", "-2% Filler Words")
            f3.metric("STAR Structural Compliance", "88%", "Excellent Matrix Mapping")
            
            if st.button("Reset Simulation Space"):
                st.session_state.interview_started = False
                st.session_state.current_question_idx = 0
                st.rerun()

# ==========================================
# MODULE 4: UNIVERSAL QUESTION BANK
# ==========================================
elif menu == "📚 Universal Question Bank":
    st.title("Enterprise Engineering Question Matrix")
    st.write("Browse, filter, and study thousands of indexed technical and core leadership questions.")
    
    q_cat = st.tabs(["System Design", "Data Structures & Algorithms", "Behavioral Leadership", "Cloud Engineering"])
    
    with q_cat[0]:
        st.markdown("### System Design Challenges")
        with st.expander("1. Design an enterprise global rate-limiter for a multi-tenant SaaS application."):
            st.markdown("""
            * **Target Core Concepts:** Token Bucket vs Leaky Bucket algorithms, Redis Cluster storage layer, Edge network termination.
            * **Ideal Architectural Vector:** Discuss latency impacts, failure safety states (fail-open vs fail-closed), and cryptographic token checks at proxy layers.
            """)
        with st.expander("2. Architect a real-time analytics aggregation matrix for a platform like Twitch."):
            st.write("Focus Areas: Kafka data ingestion pipelines, Apache Flink stream processing, and distributed time-series databases.")
            
    with q_cat[1]:
        st.markdown("### Algorithmic Vector Sets")
        st.dataframe({
            "Problem Signature": ["LRU Cache Implementation", "Merge k Sorted Lists", "Network Delay Time Matrix"],
            "Difficulty Match": ["Medium", "Hard", "Medium"],
            "Target Concept": ["Data Structures", "Divide & Conquer", "Graph Analytics / Dijkstra"],
            "Success Metric": ["84%", "41%", "67%"]
        }, use_container_width=True)

# ==========================================
# MODULE 5: AI CAREER ASSISTANT
# ==========================================
elif menu == "💬 AI Career Assistant":
    st.title("Nexus AI Copilot Workspace")
    st.write("Interact with your persistent career strategic execution model for real-time code execution debugging, compensation negotiation, and tactical guidance.")
    
    # Showcase interactive persistent chat component
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("Ask about architecture concepts, counter-offer scripting, or interview recovery tactics..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Simulated Streaming Vector Response from Model
            ai_responses = [
                f"Analyzing prompt framework... For standard compensation packages tracking at enterprise tiers matching your targets, you should demand a base structure indexing at the 75th percentile, coupled with non-overlapping equity vesting schedules. Let me draft a counter-proposal script for you.",
                f"Regarding that architectural concept: implementing a circuit-breaker pattern here prevents downstream cascading failures across your distributed application. Let's write out the mock implementation in Python to demonstrate this to your interviewer."
            ]
            response_text = random.choice(ai_responses)
            
            for chunk in response_text.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})
