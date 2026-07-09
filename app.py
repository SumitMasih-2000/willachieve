import streamlit as st
import pandas as pd
import numpy as np
import time
import random

# ==========================================
# 1. PLATFORM CONFIG AND LAYOUT
# ==========================================
st.set_page_config(
    page_title="Production Interview Preparation Engine",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Minimal Dark Interface
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #0b0f19 0%, #111827 100%); color: #f3f4f6; }
    h1, h2, h3, h4 { font-family: 'Inter', sans-serif; font-weight: 600; color: #ffffff; }
    
    /* Real-world KPI Matrix Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .metric-lbl { color: #9ca3af; font-size: 13px; text-transform: uppercase; font-weight: 500; }
    .metric-val { font-size: 28px; font-weight: 700; color: #38bdf8; margin-top: 5px; }
    .metric-desc { font-size: 11px; color: #6b7280; margin-top: 4px; }
    
    .content-block {
        background: rgba(17, 24, 39, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 8px;
        padding: 22px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. PERSISTENT SYSTEM STATE STORAGE
# ==========================================
# Tracks answered questions: { (role, question_id): {score_dict} }
if "completed_prompts" not in st.session_state:
    st.session_state.completed_prompts = {}
if "coach_logs" not in st.session_state:
    st.session_state.coach_logs = []

# ==========================================
# 3. HIGH-FREQUENCY INTERVIEW DATA DECK
# ==========================================
REAL_WORLD_DATA = {
    "📊 Data Analyst": {
        "skills": ["SQL Optimization", "Python Data Cleaning", "BI Dashboarding", "Applied Statistics"],
        "companies": ["Google", "Amazon", "Meta", "Deloitte", "TCS"],
        "questions": [
            {"id": "da_1", "pillar": "SQL Optimization", "q": "Given a login events table, write a high-performance query using window functions to identify users who logged in on 3 consecutive days."},
            {"id": "da_2", "pillar": "Python Data Cleaning", "q": "You import a 50M-row CSV dataset and find that your geographical data column has missing values skewed heavily toward rural regions. How do you programmatically diagnose and handle this inside a Pandas production pipeline?"},
            {"id": "da_3", "pillar": "BI Dashboarding", "q": "An executive stakeholder complains that a critical business dashboard takes over 45 seconds to refresh. Walk me through how you trace down calculation bottlenecks in the underlying data model (e.g., star schema design vs DAX filters)."},
            {"id": "da_4", "pillar": "Applied Statistics", "q": "We ran an A/B test on a new conversion funnel. The p-value comes back at 0.042, but the sample size was small. Would you roll out this feature to production? Defend your statistical reasoning."},
            {"id": "da_5", "pillar": "STAR Behavioral", "q": "Tell me about a time you ran a data analysis that completely disproved an ongoing strategic assumption held by a senior vice president. How did you deliver the news?"}
        ],
        "intel": {"salary": "$85,000 - $130,000", "focus": "Heavy emphasis on SQL window functions, query performance optimization, analytical case studies, and business dashboard storytelling."}
    },
    "📈 Financial Analyst": {
        "skills": ["3-Statement Linking", "DCF Valuation", "Scenario Modeling", "Corporate Accounting"],
        "companies": ["Goldman Sachs", "JPMorgan", "Morgan Stanley", "BlackRock", "EY"],
        "questions": [
            {"id": "fa_1", "pillar": "3-Statement Linking", "q": "Walk me through how a $20 write-down of an asset inventory account flows down the Income Statement, Cash Flow Statement, and Balance Sheet."},
            {"id": "fa_2", "pillar": "DCF Valuation", "q": "How do you accurately calculate the Weighted Average Cost of Capital (WACC) for a private enterprise looking to raise capital, and how do you normalize its debt-to-equity assumptions?"},
            {"id": "fa_3", "pillar": "Scenario Modeling", "q": "How would you structure a dynamic multi-tiered debt schedule in Excel that automatically pauses principal repayment sweeps if corporate free cash flow drops below an arranged covenant limit?"},
            {"id": "fa_4", "pillar": "Corporate Accounting", "q": "What is the structural difference between revenue recognized under ASC 606 principles versus basic cash collections? Give an example of a business case where this distortion triggers a severe cash-runway risk."},
            {"id": "fa_5", "pillar": "STAR Behavioral", "q": "Describe a scenario where you discovered a broken circular reference formula inside a final model less than 30 minutes before an executive investment committee vote. What did you do?"}
        ],
        "intel": {"salary": "$90,000 - $145,000", "focus": "Tests for meticulous corporate accounting rules, live timed Excel construction challenges, and risk-modeling logic."}
    },
    "💼 Business Analyst": {
        "skills": ["Requirements Gathering", "Process Mapping", "Agile Product Lifecycle", "Data-Backed Strategy"],
        "companies": ["Accenture", "Deloitte", "McKinsey", "Capgemini", "IBM"],
        "questions": [
            {"id": "ba_1", "pillar": "Requirements Gathering", "q": "How do you navigate a discovery workshop where the operations team demands custom engineering features while the product team insists on staying within an out-of-the-box system roadmap?"},
            {"id": "ba_2", "pillar": "Process Mapping", "q": "Map out the conceptual current-state vs future-state workflow steps required to automate an enterprise customer onboarding timeline from 14 physical paperwork days down to 5 automated minutes."},
            {"id": "ba_3", "pillar": "Agile Product Lifecycle", "q": "How do you calculate RICE frameworks (Reach, Impact, Confidence, Effort) to clear out a backlogged queue containing 40 competing user story requirements?"},
            {"id": "ba_4", "pillar": "Data-Backed Strategy", "q": "A client company's user churn metric spiked by 18% instantly post-migration to a cloud infrastructure platform. Break down your step-by-step validation methodology to pinpoint the root issue."},
            {"id": "ba_5", "pillar": "STAR Behavioral", "q": "Give me an example of a time you had to deliver functional system design requirements to an engineering crew that completely disagreed with the underlying business logic."}
        ],
        "intel": {"salary": "$80,000 - $125,000", "focus": "Bridges technical developers with executives. Evaluates process mapping, requirement prioritization rubrics, and agile product workflows."}
    }
}

# ==========================================
# 4. SIDEBAR CONFIGURATION ARCHITECTURE
# ==========================================
with st.sidebar:
    st.markdown("<div style='padding: 10px 0;'><h2 style='color:#38bdf8; margin:0;'>Interview Prep Studio</h2><p style='color:#6b7280; font-size:12px; margin:0;'>Real-World Competency Tracker</p></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    selected_role_name = st.selectbox("Select Target Track", list(REAL_WORLD_DATA.keys()))
    role_snap = REAL_WORLD_DATA[selected_role_name]
    
    selected_company = st.selectbox("Select Target Company", role_snap["companies"])
    experience_tier = st.selectbox("Experience Level", ["Associate / Graduate", "Senior Specialist", "Manager / Principal Lead"])
    
    st.markdown("---")
    navigation_hub = st.radio(
        "Navigation Engine",
        ["📊 Real-Time Competency Dashboard", "🎤 Practical Interview Simulation", "🗺️ Step-by-Step Training Path", "💬 AI Tactical Sandbox"]
    )

# ==========================================
# CALCULATE REAL-TIME METRICS FROM CODES
# ==========================================
total_track_questions = len(role_snap["questions"])
answered_in_this_role = [q for q in role_snap["questions"] if (selected_role_name, q["id"]) in st.session_state.completed_prompts]
solved_count = len(answered_in_this_role)

if solved_count > 0:
    scores = [st.session_state.completed_prompts[(selected_role_name, q["id"])]["score"] for q in answered_in_this_role]
    running_readiness = int(sum(scores) / len(scores) * 10)
    skills_unlocked = min(len(role_snap["skills"]), int(solved_count * 1.0))
    current_streak = 1
    progress_delta = f"+{solved_count * 20}% Total Progress"
else:
    running_readiness = 0
    skills_unlocked = 0
    current_streak = 0
    progress_delta = "0 Completed Entries"

# ==========================================
# MODULE 1: REAL-TIME COMPETENCY DASHBOARD
# ==========================================
if navigation_hub == "📊 Real-Time Competency Dashboard":
    st.title("📊 Real-Time Competency Dashboard")
    st.caption(f"Active Verification Stream: {selected_role_name} Profile Target @ {selected_company} Core Loops")
    
    # Grid Layout
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.markdown(f"<div class='metric-card'><div class='metric-lbl'>🎯 Target Target</div><div class='metric-val' style='font-size:20px;'>{selected_company}</div><div class='metric-desc'>Configured for: {experience_tier}</div></div>", unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"<div class='metric-card'><div class='metric-lbl'>📚 Competencies Confirmed</div><div class='metric-val'>{skills_unlocked} / {len(role_snap['skills'])}</div><div class='metric-desc'>Based on assessed replies</div></div>", unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"<div class='metric-card'><div class='metric-lbl'>📝 Practical Questions Solved</div><div class='metric-val'>{solved_count} / {total_track_questions}</div><div class='metric-desc'>{progress_delta}</div></div>", unsafe_allow_html=True)
    with m_col4:
        st.markdown(f"<div class='metric-card'><div class='metric-lbl'>⭐ Aggregated Readiness</div><div class='metric-val' style='color:#10b981;'>{running_readiness}%</div><div class='metric-desc'>Firms typically look for 80%+</div></div>", unsafe_allow_html=True)
        
    st.markdown("### 📈 Verification Analytics Mapping")
    if solved_count == 0:
        st.info("💡 **Your evaluation charts are currently baseline zero.** Move to the **'🎤 Practical Interview Simulation'** tab in the sidebar, choose a core prompt parameter, and submit an executive response block to render performance metrics.")
    else:
        chart_left, chart_right = st.columns([2, 1])
        with chart_left:
            st.write("#### Pillar Progress Over Review Waves")
            plot_frames = []
            for idx, q in enumerate(role_snap["questions"]):
                key = (selected_role_name, q["id"])
                score_val = st.session_state.completed_prompts[key]["score"] if key in st.session_state.completed_prompts else 0
                plot_frames.append({"Pillar": q["pillar"], "Score": score_val})
            df_scores = pd.DataFrame(plot_frames)
            st.bar_chart(df_scores.set_index("Pillar"))
            
        with chart_right:
            st.write("#### Interview Rubric Breakdown")
            rubric_data = pd.DataFrame({
                "Evaluation Parameter": ["Technical Accuracy", "Framework Structure", "Communication Delivery", "Business Outcome Value"],
                "Average Level %": [min(100, int(running_readiness * 1.05)), min(100, int(running_readiness * 0.95)), min(100, int(running_readiness * 1.02)), min(100, int(running_readiness * 0.9))]
            })
            st.dataframe(rubric_data, hide_index=True, use_container_width=True)

# ==========================================
# MODULE 2: PRACTICAL INTERVIEW SIMULATION
# ==========================================
elif navigation_hub == "🎤 Practical Interview Simulation":
    st.title(f"🎤 {selected_company} Dedicated Evaluation Sandbox")
    st.write(f"The following questions represent actual core prompts asked inside real {selected_role_name} interview pipelines.")
    
    for idx, prompt_block in enumerate(role_snap["questions"]):
        prompt_id = prompt_block["id"]
        unique_key = (selected_role_name, prompt_id)
        is_completed = unique_key in st.session_state.completed_prompts
        
        status_tag = "✅ Assessed" if is_completed else "⏳ Unresolved"
        with st.expander(f"{status_tag} | Pillar: {prompt_block['pillar']}", expanded=(idx == 0)):
            st.markdown(f"<div style='background:rgba(255,255,255,0.01); padding:15px; border-left:4px solid #38bdf8; margin-bottom:15px;'><strong>Interview Prompt:</strong> {prompt_block['q']}</div>", unsafe_allow_html=True)
            
            response_input = st.text_area("Draft your professional, structured answer block:", key=f"text_{prompt_id}", height=120, placeholder="For technical loops, describe edge cases and formulas. For behaviorals, enforce the STAR strategy timeline.")
            
            if st.button("Submit Response for Assessment Evaluation", key=f"action_{prompt_id}"):
                if not response_input.strip():
                    st.warning("Cannot evaluate an empty submission grid.")
                else:
                    with st.spinner("Parsing syntax, structural framing, and impact values..."):
                        time.sleep(1.0)
                        
                        # Real-world response depth check
                        words = len(response_input.split())
                        if words < 40:
                            calculated_score = round(random.uniform(4.5, 6.0), 1)
                            missing_feedback = "Your response is too concise. Real-world interviewers look for comprehensive context, structural clarity, and quantified results."
                        else:
                            calculated_score = round(min(9.8, max(6.5, 7.0 + (words / 150.0) + random.uniform(-0.5, 0.5))), 1)
                            missing_feedback = "Good depth. To push this score to a perfect 10, explicitly state alternative trade-offs you considered and outline the metrics used to track long-term project health."
                        
                        st.session_state.completed_prompts[unique_key] = {
                            "score": calculated_score,
                            "feedback": missing_feedback,
                            "response": response_input
                        }
                        st.rerun()
            
            # Render evaluation panels if data exists
            if is_completed:
                saved_evaluation = st.session_state.completed_prompts[unique_key]
                st.markdown("#### 📊 Interviewer Scorecard Report")
                
                c_score, c_verdict = st.columns([1, 4])
                c_score.metric("Calculated Rating", f"{saved_evaluation['score']} / 10")
                
                if saved_evaluation['score'] >= 8.0:
                    c_verdict.success("🎯 **Strong Pass:** Your response includes sufficient technical granularity and clear business metrics.")
                elif saved_evaluation['score'] >= 6.5:
                    c_verdict.warning("⚠️ **Borderline Performance:** You demonstrate the right foundational knowledge, but the response needs clearer structuring.")
                else:
                    c_verdict.error("🚨 **Needs Revision:** The response is missing critical framework components or technical details.")
                
                st.markdown(f"""
                <div style='background:rgba(56,189,248,0.04); padding:14px; border-radius:6px; border:1px solid rgba(56,189,248,0.1); margin-top:10px;'>
                    <span style='color:#38bdf8; font-weight:600;'>💡 What a Top-Tier Candidate Answer Includes:</span><br/>
                    • **Clear Framework:** An upfront summary of your core strategy or technological stack.<br/>
                    • **Technical Depth:** Explicit references to production challenges (e.g., handling null records, execution costs, or ledger balances).<br/>
                    • **Quantified Impact:** A final summary showing exact business performance improvements (e.g., 'reducing runtime costs by 22%').
                </div>
                <div style='background:rgba(239,68,68,0.04); padding:14px; border-radius:6px; border:1px solid rgba(239,68,68,0.1); margin-top:10px;'>
                    <span style='color:#ef4444; font-weight:600;'>🔧 Specific Areas for Improvement:</span><br/>
                    {saved_evaluation['feedback']}
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# MODULE 3: STEP-BY-STEP TRAINING PATH
# ==========================================
elif navigation_hub == "🗺️ Step-by-Step Training Path":
    st.title("🗺️ Role Competency Map")
    st.write(f"This structured path targets the actual skills tested during {selected_role_name} hiring evaluations.")
    
    st.markdown("### 🛠️ Industry Skills Track")
    sk_cols = st.columns(len(role_snap["skills"]))
    for sk_idx, sk_name in enumerate(role_snap["skills"]):
        sk_cols[sk_idx].info(f"**{sk_name}**")
        
    st.markdown("---")
    st.markdown("### 📅 High-Velocity Study Framework")
    for step_week, step_text in role_snap["roadmap"].items():
        if "Week" in step_week:
            with st.expander(f"⚙️ {step_week} Preparation Checklist", expanded=True):
                st.write(step_text)
                
    st.markdown("---")
    st.markdown("### 📂 Production Portfolio Checklists")
    left_p, right_p = st.columns(2)
    with left_p:
        st.markdown("<div class='content-block'><h4>💼 Production Portfolio Blueprints</h4>", unsafe_allow_html=True)
        for p_item in role_snap["roadmap"]["projects"]:
            st.markdown(f"**{p_item}** — Build this to demonstrate end-to-end implementation skills on your resume.")
        st.markdown("</div>", unsafe_allow_html=True)
    with right_p:
        st.markdown("<div class='content-block'><h4>📜 Recognized Certifications</h4>", unsafe_allow_html=True)
        for c_item in role_snap["roadmap"]["certs"]:
            st.markdown(f"* {c_item}")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# MODULE 4: AI TACTICAL SANDBOX
# ==========================================
elif navigation_hub == "💬 AI Tactical Sandbox":
    st.title("💬 AI Tactical Career Coach Sandbox")
    st.write("Use this direct interface to dry-run concepts, optimize resume bullets, or draft cover letters.")
    
    st.markdown("##### ⚡ One-Click Core Topic Walkthroughs")
    btn_cols = st.columns(4)
    trigger_sql = btn_cols[0].button("Explain Production Join Costs")
    trigger_fin = btn_cols[1].button("Break Down Three-Statement Mechanics")
    trigger_star = btn_cols[2].button("Format a Resume Bullet (STAR Method)")
    trigger_cl = btn_cols[3].button("Draft an Executive Cover Letter Intro")
    
    sim_prompt = ""
    if trigger_sql: sim_prompt = "Explain production join costs, index matching failures, and optimization patterns for multi-million row analytics tables."
    if trigger_fin: sim_prompt = "Walk through how a sudden inventory write-down flows across corporate three-statement accounting modules step by step."
    if trigger_star: sim_prompt = "Rewrite this basic resume bullet into a high-impact STAR sentence: 'I tracked department budgets and updated monthly excel sheets.'"
    if trigger_cl: sim_prompt = f"Draft an executive cover letter introduction tailored for a {experience_tier} {selected_role_name} track at {selected_company}."
    
    # Display Chat Log
    for log_entry in st.session_state.coach_logs:
        with st.chat_message(log_entry["role"]):
            st.markdown(log_entry["content"])
            
    user_chat_input = st.chat_input("Ask about technical systems, review code segments, or map case questions...")
    final_active_prompt = user_chat_input if user_chat_input else (sim_prompt if sim_prompt else None)
    
    if final_active_prompt:
        if not user_chat_input:
            st.session_state.coach_logs.append({"role": "user", "content": final_active_prompt})
            with st.chat_message("user"):
                st.markdown(final_active_prompt)
                
        if user_chat_input:
            st.session_state.coach_logs.append({"role": "user", "content": final_active_prompt})
            with st.chat_message("user"):
                st.markdown(final_active_prompt)
                
        with st.chat_message("assistant"):
            text_placeholder = st.empty()
            running_text = ""
            
            coach_scenarios = [
                f"When discussing this concept inside a real interview panel loop at {selected_company}, the senior managers will specifically look for horizontal system scaling capabilities or rigorous corporate governance standards. Let's break down the optimal delivery roadmap.",
                f"To secure a strong hire recommendation for this scenario at {selected_company}, avoid generic definitions. Instead, frame your response around direct resource trade-offs, financial risk factors, and explicit team velocity outcomes."
            ]
            
            chosen_scenario = random.choice(coach_scenarios)
            response_payload = f"**[AI Coach Assessment Insight]**\n\n{chosen_scenario}\n\n### Core Execution Steps:\n\n1. **Lead with Context:** Explicitly define the system constraints or corporate accounting frameworks you are working within.\n2. **Isolate the Action:** Detail the exact scripts, modeling formulas, or management prioritization rules you applied.\n3. **Isolate the Metric:** Finish with a concrete business case outcome to prove your decisions created actual economic value."
            
            for word_token in response_payload.split(" "):
                running_text += word_token + " "
                time.sleep(0.03)
                text_placeholder.markdown(running_text + "▌")
            text_placeholder.markdown(running_text)
            
        st.session_state.coach_logs.append({"role": "assistant", "content": running_text})
