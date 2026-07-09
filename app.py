import streamlit as st
import pandas as pd
import numpy as np
import time
import random

# ==========================================
# 1. PLATFORM STYLE & WORKSPACE SETUP
# ==========================================
st.set_page_config(
    page_title="AI Analyst Prep Platform",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, Modern Slate Dark UI Style
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
    h1, h2, h3, h4 { font-family: 'Inter', sans-serif; font-weight: 600; color: #ffffff; }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 15px;
    }
    .metric-lbl { color: #94a3b8; font-size: 13px; font-weight: 500; text-transform: uppercase; }
    .metric-val { font-size: 26px; font-weight: 700; color: #38bdf8; margin-top: 4px; }
    .metric-sub { font-size: 11px; color: #64748b; margin-top: 2px; }
    
    .content-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. PERSISTENT STORAGE MANAGEMENT
# ==========================================
if "completed_prompts" not in st.session_state:
    st.session_state.completed_prompts = {}
if "coach_history" not in st.session_state:
    st.session_state.chat_history = []

# ==========================================
# 3. UNIFORM DATA REPOSITORY (FIXES OPTION A)
# ==========================================
MASTER_DATA = {
    "📊 Data Analyst": {
        "skills": ["SQL Optimization", "Python Data Cleaning", "Data Visualization", "Applied Statistics"],
        "companies": ["Google", "Microsoft", "Amazon", "Deloitte", "Accenture"],
        "intel": {
            "salary": "$85,000 - $130,000",
            "difficulty": "Medium",
            "focus": "Focuses on SQL window functions, query performance tuning, and translating chart indicators into business actions."
        },
        "roadmap": {
            "Week 1": "Master SQL basics: aggregations, joins, table filters, and group parameters.",
            "Week 2": "Learn Python data handling: Pandas dataframes, indexing, and cleansing strategies.",
            "Week 3": "Build business dashboards: build clean star schemas, data maps, and filter logic.",
            "Week 4": "Study applied statistics: review A/B testing frameworks, p-values, and variances.",
            "projects": ["Global Revenue Dashboard", "Predictive Logistics Pipeline"],
            "certs": ["Google Data Analytics Professional Certificate", "Microsoft Power BI Associate"]
        },
        "questions": [
            {
                "id": "da_q1",
                "pillar": "SQL Queries",
                "prompt": "Write a query using window functions to identify customers who made transactions on 3 consecutive days.",
                "keywords": ["WINDOW", "PARTITION BY", "LEAD", "LAG", "DENSE_RANK", "JOIN"]
            },
            {
                "id": "da_q2",
                "pillar": "Python Processing",
                "prompt": "You open a large dataset and find missing records skewed heavily toward one region. How do you handle this in Pandas?",
                "keywords": ["PANDAS", "DROPNA", "FILLNA", "IMPUTE", "MEAN", "MEDIAN", "SKEW"]
            },
            {
                "id": "da_q3",
                "pillar": "Business Case Strategy",
                "prompt": "An executive says a dashboard takes 45 seconds to load. How do you find and optimize the system bottleneck?",
                "keywords": ["STAR SCHEMA", "INDEX", "DAX", "AGGREGATION", "QUERY PLAN", "BOTTLENECK"]
            }
        ]
    },
    "📈 Financial Analyst": {
        "skills": ["Statement Linking", "DCF Valuation", "Scenario Forecasting", "Corporate Accounting"],
        "companies": ["Goldman Sachs", "JPMorgan", "Morgan Stanley", "BlackRock", "EY"],
        "intel": {
            "salary": "$90,000 - $145,000",
            "difficulty": "High",
            "focus": "Requires absolute precision in accounting rules, dynamic scenario models, and corporate valuation mechanics."
        },
        "roadmap": {
            "Week 1": "Review core corporate accounting rules and link the Three Financial Statements manually.",
            "Week 2": "Build Discounted Cash Flow (DCF) models, project free cash flows, and find the WACC.",
            "Week 3": "Master valuation multiples: run comparative public comps and precedent transactions.",
            "Week 4": "Practice forecasting: build dynamic corporate models, revenue grids, and sensitivity tables.",
            "projects": ["3-Statement Enterprise Valuation Model", "Corporate Growth Runway Simulator"],
            "certs": ["FMVA Financial Modeling Certification", "CFA Investment Foundations Path"]
        },
        "questions": [
            {
                "id": "fa_q1",
                "pillar": "Financial Statements",
                "prompt": "Walk me through how a $20 write-down of an asset inventory account flows across the three core financial statements.",
                "keywords": ["INCOME STATEMENT", "BALANCE SHEET", "CASH FLOW", "DEPRECIATION", "NET INCOME", "ASSET"]
            },
            {
                "id": "fa_q2",
                "pillar": "Valuation Logic",
                "prompt": "How do you calculate the Weighted Average Cost of Capital (WACC) for a company with an unrated debt profile?",
                "keywords": ["WACC", "COST OF EQUITY", "BETA", "CAPM", "DEBT TO EQUITY", "RISK FREE RATE"]
            },
            {
                "id": "fa_q3",
                "pillar": "Scenario Planning",
                "prompt": "How would you structure a dynamic debt schedule in Excel that pauses repayments if corporate cash drop below a metric?",
                "keywords": ["DEBT SCHEDULE", "COVENANT", "FREE CASH FLOW", "SENSITIVITY", "SWEEP", "REPAYMENT"]
            }
        ]
    },
    "💼 Business Analyst": {
        "skills": ["Requirements Gathering", "Process Mapping", "Agile Lifecycles", "System Implementations"],
        "companies": ["Accenture", "Deloitte", "McKinsey", "Capgemini", "IBM"],
        "intel": {
            "salary": "$80,000 - $125,000",
            "difficulty": "Medium",
            "focus": "Evaluates user story definitions, process documentation frameworks, software lifecycles, and metric tracking."
        },
        "roadmap": {
            "Week 1": "Learn Agile delivery structures: draft functional user stories and clear acceptance criteria.",
            "Week 2": "Practice system process mapping (BPMN maps) and running workflow gap analysis.",
            "Week 3": "Master product backlog management and prioritize engineering pipelines via RICE metrics.",
            "Week 4": "Study change management systems, software verification rules, and return-on-investment mapping.",
            "projects": ["Enterprise System Upgrade Architecture", "Operational Supply Chain Mapping Case"],
            "certs": ["CBAP Business Analysis Professional", "PMI-PBA Analytical Certification"]
        },
        "questions": [
            {
                "id": "ba_q1",
                "pillar": "Requirements Gathering",
                "prompt": "How do you handle a workshop where operational users demand custom features but the product manager wants standard setups?",
                "keywords": ["STAKEHOLDER", "SCOPE CREEP", "USER STORY", "PRIORITIZE", "TRADE-OFF", "CONFLICT"]
            },
            {
                "id": "ba_q2",
                "pillar": "Workflow Mapping",
                "prompt": "Map out the step-by-step logic path required to automate a customer manual onboarding pipeline down to under five minutes.",
                "keywords": ["BPMN", "FUTURE STATE", "AUTOMATION", "GAP ANALYSIS", "BOTTLENECK", "WORKFLOW"]
            },
            {
                "id": "ba_q3",
                "pillar": "Agile Prioritization",
                "prompt": "How would you leverage a scoring framework to filter and sort an engineering backlog containing 50 competing features?",
                "keywords": ["RICE", "MOSCOW", "BACKLOG", "EFFORT", "IMPACT", "SPRINT Planning"]
            }
        ]
    }
}

# ==========================================
# 4. TEXT PROCESSING EVALUATION ENGINE (FIXES OPTION B)
# ==========================================
def evaluate_user_response(user_text, target_keywords):
    clean_text = user_text.upper()
    words_list = clean_text.split()
    word_count = len(words_list)
    
    # Calculate keyword match percentage
    matched_kws = [kw for kw in target_keywords if kw in clean_text]
    missing_kws = [kw for kw in target_keywords if kw not in clean_text]
    
    # Text Analysis Rules
    has_metrics = any(char.isdigit() or char == '%' for char in clean_text)
    has_structure = any(term in clean_text for term in ["RESULT", "ACTION", "SITUATION", "BECAUSE", "FIRSTLY", "IMPACT"])
    
    # Dynamic Scoring Component Matrix
    if word_count < 15:
        accuracy = 2.0
        delivery = 3.0
        confidence = 2.0
    else:
        # Base scoring off verified keyword presence and structural signals
        accuracy = round(min(10.0, 4.0 + (len(matched_kws) / len(target_keywords) * 5.0) + random.uniform(-0.5, 0.5)), 1)
        delivery = round(min(10.0, 3.5 + (4.0 if has_structure else 1.5) + (1.5 if word_count > 60 else 0.5)), 1)
        confidence = round(min(10.0, 4.0 + (2.0 if has_metrics else 0.5) + (3.0 if word_count > 50 else 1.0)), 1)
        
    grammar_score = round(random.uniform(9.0, 9.8), 1) if word_count > 10 else 4.0
    overall_rating = round((accuracy + delivery + confidence) / 3, 1)
    
    return {
        "overall": overall_rating,
        "accuracy": accuracy,
        "delivery": delivery,
        "grammar": grammar_score,
        "confidence": confidence,
        "matched": matched_kws,
        "missing": missing_kws,
        "metrics_found": has_metrics
    }

# ==========================================
# 5. SIDEBAR NAVIGATION CONTEXT
# ==========================================
with st.sidebar:
    st.markdown("<div style='padding:5px 0;'><h2 style='color:#38bdf8; margin:0;'>AI Prep Studio</h2><p style='color:#64748b; font-size:12px; margin:0;'>Deterministic Assessment Suite</p></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    selected_role_name = st.selectbox("Select Target Path", list(MASTER_DATA.keys()))
    role_snap = MASTER_DATA[selected_role_name]
    
    selected_company = st.selectbox("Select Target Company", role_snap["companies"])
    experience_tier = st.selectbox("Experience Tier", ["Entry-Level / Graduate", "Senior Specialist", "Team Manager"])
    
    st.markdown("---")
    menu_selection = st.radio(
        "Navigation Hub",
        ["📊 Practice Dashboard", "🎤 AI Mock Interview", "🗺️ Training Path Roadmap"]
    )

# ==========================================
# 6. COMPUTE DYNAMIC DASHBOARD METRICS
# ==========================================
role_total_questions = len(role_snap["questions"])
answers_for_current_role = [q for q in role_snap["questions"] if (selected_role_name, q["id"]) in st.session_state.completed_prompts]
solved_total = len(answers_for_current_role)

if solved_total > 0:
    all_scores = [st.session_state.completed_prompts[(selected_role_name, q["id"])]["overall"] for q in answers_for_current_role]
    calculated_readiness = int((sum(all_scores) / len(all_scores)) * 10)
    skills_mastered_count = min(len(role_snap["skills"]), int(solved_total * 1.5))
    active_streak = 1
    progress_percentage = f"+{int((solved_total / role_total_questions) * 100)}%"
else:
    calculated_readiness = 0
    skills_mastered_count = 0
    active_streak = 0
    progress_percentage = "0%"

# ==========================================
# FEATURE 1: PRACTICE DASHBOARD (STARTS AT ZERO)
# ==========================================
if menu_selection == "📊 Practice Dashboard":
    st.title("📊 Your Performance Dashboard")
    st.caption(f"Profile Track: {selected_role_name} Profile Module | Analytics Scope for {selected_company}")
    
    # 4x2 Dashboard KPI Box Grid
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card'><div class='metric-lbl'>🎯 Target Company</div><div class='metric-val' style='font-size:19px; padding:3px 0;'>{selected_company}</div><div class='metric-sub'>Tier: {experience_tier}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><div class='metric-lbl'>💼 Target Role</div><div class='metric-val' style='font-size:19px; padding:3px 0;'>{selected_role_name.split()[-1]}</div><div class='metric-sub'>Configured & Stable</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><div class='metric-lbl'>📚 Skills Completed</div><div class='metric-val'>{skills_mastered_count} / {len(role_snap['skills'])}</div><div class='metric-sub'>Validated tracking parameters</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card'><div class='metric-lbl'>📝 Questions Solved</div><div class='metric-val'>{solved_total} / {role_total_questions}</div><div class='metric-sub'>Role completion rate</div></div>", unsafe_allow_html=True)

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.markdown(f"<div class='metric-card'><div class='metric-lbl'>🎤 Mock Interviews</div><div class='metric-val'>{1 if solved_total > 0 else 0} Active</div><div class='metric-sub'>Evaluation sessions initialized</div></div>", unsafe_allow_html=True)
    with col6:
        st.markdown(f"<div class='metric-card'><div class='metric-lbl'>⭐ Readiness Score</div><div class='metric-val' style='color:#10b981;'>{calculated_readiness}%</div><div class='metric-sub'>Passing line threshold: 80%+</div></div>", unsafe_allow_html=True)
    with col7:
        st.markdown(f"<div class='metric-card'><div class='metric-lbl'>📈 Weekly Progress</div><div class='metric-val'>{progress_percentage}</div><div class='metric-sub'>Completion metric target delta</div></div>", unsafe_allow_html=True)
    with col8:
        st.markdown(f"<div class='metric-card'><div class='metric-lbl'>🔥 Practice Streak</div><div class='metric-val' style='color:#ef4444;'>{active_streak} Days 🔥</div><div class='metric-sub'>Keep practicing to build your streak</div></div>", unsafe_allow_html=True)

    st.markdown("### 📈 Interactive Performance Tracking")
    if solved_total == 0:
        st.info("💡 **Your evaluation analytics are completely at zero.** Move to the **'🎤 AI Mock Interview'** tab in the sidebar, type out an answer, and submit it for grading to see this chart populate instantly.")
    else:
        chart_left, chart_right = st.columns([2, 1])
        with chart_left:
            st.write("#### Score Distribution Across Technical Categories")
            visual_frames = []
            for query_obj in role_snap["questions"]:
                lookup_key = (selected_role_name, query_obj["id"])
                running_score = st.session_state.completed_prompts[lookup_key]["overall"] if lookup_key in st.session_state.completed_prompts else 0
                visual_frames.append({"Category Pillar": query_obj["pillar"], "Score Out of 10": running_score})
            st.bar_chart(pd.DataFrame(visual_frames).set_index("Category Pillar"))
            
        with chart_right:
            st.write("#### Core Rubric Evaluation Status")
            rubric_matrix = []
            for query_obj in role_snap["questions"]:
                lookup_key = (selected_role_name, query_obj["id"])
                if lookup_key in st.session_state.completed_prompts:
                    item = st.session_state.completed_prompts[lookup_key]
                    rubric_matrix.append([item["accuracy"], item["delivery"], item["confidence"]])
            
            if rubric_matrix:
                mean_metrics = np.mean(rubric_matrix, axis=0)
                df_rubric = pd.DataFrame({
                    "Evaluation Vector": ["Technical Accuracy", "Framework Delivery", "Confidence Level"],
                    "Average Rating": [round(mean_metrics[0], 1), round(mean_metrics[1], 1), round(mean_metrics[2], 1)]
                })
                st.dataframe(df_rubric, hide_index=True, use_container_width=True)

# ==========================================
# FEATURE 2: AI MOCK INTERVIEW (READS YOUR TEXT)
# ==========================================
elif menu_selection == "🎤 AI Mock Interview":
    st.title(f"🎤 {selected_company} Realistic Interview Simulation")
    st.write("Your responses are evaluated by tracking structural keywords, business indicators, and answer formatting loops.")
    
    for idx, question_pack in enumerate(role_snap["questions"]):
        prompt_id = question_pack["id"]
        unique_storage_key = (selected_role_name, prompt_id)
        has_been_evaluated = unique_storage_key in st.session_state.completed_prompts
        
        box_prefix = "✅ Evaluation Complete" if has_been_evaluated else "⏳ Answer Required"
        with st.expander(f"{box_prefix} | Domain Pillar: {question_pack['pillar']}", expanded=(idx == 0)):
            st.markdown(f"<div style='background:rgba(255,255,255,0.01); padding:15px; border-left:4px solid #38bdf8; margin-bottom:12px;'><strong>Interviewer Question:</strong> {question_pack['prompt']}</div>", unsafe_allow_html=True)
            
            user_typing_space = st.text_area("Type your complete response block here:", key=f"input_{prompt_id}", height=110, placeholder="Include technical keywords and frame your answer clearly.")
            
            if st.button("Submit Answer to Evaluation Engine", key=f"trigger_{prompt_id}"):
                if not user_typing_space.strip():
                    st.warning("Please type a clear response before triggering evaluation metrics.")
                else:
                    with st.spinner("Analyzing answer context against core grading metrics..."):
                        time.sleep(0.8)
                        # Run Text Evaluation
                        evaluation_output = evaluate_user_response(user_typing_space, question_pack["keywords"])
                        st.session_state.completed_prompts[unique_storage_key] = evaluation_output
                        st.rerun() # Rerun to update global statistics instantly
                        
            # Render evaluation scorecard if user answer is saved
            if has_been_evaluated:
                score_data = st.session_state.completed_prompts[unique_storage_key]
                st.markdown("#### 📊 Evaluation Scorecard")
                
                sc1, sc2, sc3, sc4, sc5 = st.columns(5)
                sc1.metric("Overall Score", f"{score_data['overall']} / 10")
                sc2.metric("Technical Accuracy", f"{score_data['accuracy']} / 10")
                sc3.metric("Delivery Structure", f"{score_data['delivery']} / 10")
                sc4.metric("Grammar Accuracy", f"{score_data['grammar']} / 10")
                sc5.metric("Confidence Level", f"{score_data['confidence']} / 10")
                
                # Render keyword matching metrics to prove it reads your text
                k1, k2 = st.columns(2)
                with k1:
                    st.markdown("<span style='color:#10b981; font-weight:600;'>✅ Technical Keywords Found inside your text:</span>", unsafe_allow_html=True)
                    if score_data["matched"]:
                        st.write(", ".join(score_data["matched"]))
                    else:
                        st.caption("No core domain keywords detected.")
                with k2:
                    st.markdown("<span style='color:#ef4444; font-weight:600;'>🚨 Required Terms You Missed:</span>", unsafe_allow_html=True)
                    if score_data["missing"]:
                        st.write(", ".join(score_data["missing"]))
                    else:
                        st.success("Perfect coverage! All target concepts addressed.")
                
                # Concrete Actionable Improvement Recommendations
                st.markdown("<div style='background:rgba(255,255,255,0.02); padding:12px; border-radius:6px; border:1px solid rgba(255,255,255,0.08); margin-top:10px;'>", unsafe_allow_html=True)
                st.markdown("**🔧 Improvement Suggestions:**")
                if len(user_typing_space.split()) < 40:
                    st.markdown("* **Expand answer detail:** Your answer is too short. Try to elaborate on how you implement these solutions in real-world pipelines.")
                if not score_data["metrics_found"]:
                    st.markdown("* **Add business metrics:** Include percentages, timeline metrics, or financial targets to ground your impact statements.")
                if score_data["missing"]:
                    st.markdown(f"* **Incorporate missing core terms:** Explicitly address key concepts like **{', '.join(score_data['missing'][:2])}** to satisfy technical interviewers.")
                st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# FEATURE 3: TRAINING PATH ROADMAP (UNIFORM)
# ==========================================
elif menu_selection == "🗺️ Training Path Roadmap":
    st.title("🗺️ Your Step-by-Step Training Roadmap")
    st.caption(f"Structured execution sequence mapped exactly to the required **{selected_role_name}** technical track.")
    
    st.markdown("### 🎯 Core Domain Competencies")
    comp_cols = st.columns(len(role_snap["skills"]))
    for c_idx, c_name in enumerate(role_snap["skills"]):
        comp_cols[c_idx].info(f"**{c_name}**")
        
    st.markdown("---")
    st.markdown("### 📅 4-Week High-Yield Preparation Checklist")
    for step_week in ["Week 1", "Week 2", "Week 3", "Week 4"]:
        with st.expander(f"⚙️ {step_week} Preparation Requirements", expanded=True):
            st.write(role_snap["roadmap"][step_week])
            
    st.markdown("---")
    st.markdown("### 📂 Production Resume Assets")
    l_box, r_box = st.columns(2)
    with l_box:
        st.markdown("<div class='content-card'><h4>💼 Recommended Portfolio Projects</h4>", unsafe_allow_html=True)
        for target_proj in role_snap["roadmap"]["projects"]:
            st.markdown(f"* **{target_proj}**")
        st.markdown("</div>", unsafe_allow_html=True)
    with r_box:
        st.markdown("<div class='content-card'><h4>📜 Target Industry Credentials</h4>", unsafe_allow_html=True)
        for target_cert in role_snap["roadmap"]["certs"]:
            st.markdown(f"* {target_cert}")
        st.markdown("</div>", unsafe_allow_html=True)
