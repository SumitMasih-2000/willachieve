import streamlit as st
import pandas as pd
import numpy as np
import time
import random

# ==========================================
# 1. PLATFORM CONFIGURATION & STYLING ENGINE
# ==========================================
st.set_page_config(
    page_title="Nexus AI - Analyst & Finance Prep",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enterprise Dark-Mode Glassmorphism Design System
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #090d16 0%, #111827 100%); color: #f3f4f6; }
    h1, h2, h3, h4 { font-family: 'Inter', sans-serif; font-weight: 700; color: #ffffff; }
    
    /* Premium KPI Glass Cards */
    .kpi-container {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
    }
    .kpi-title { color: #9ca3af; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; }
    .kpi-value { font-size: 26px; font-weight: 800; color: #6366f1; }
    .kpi-sub { font-size: 11px; color: #10b981; margin-top: 2px; }
    
    /* Feature Tabs/Borders */
    .section-card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
    }
    
    .badge-vip {
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
        color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. ANALYST & FINANCE MASTER REPOSITORY
# ==========================================
ROLE_DATA = {
    "📊 Data Analyst": {
        "companies": ["Google", "Microsoft", "Amazon", "Deloitte", "Accenture", "PwC", "EY", "KPMG", "TCS", "Infosys"],
        "skills": ["Excel", "SQL", "Python", "Power BI", "Tableau", "Statistics", "Data Cleaning", "Data Visualization"],
        "rounds": ["Resume Screening", "Aptitude", "SQL Live Assessment", "Excel Processing Test", "Python Programming", "Dashboard Case Study", "HR Executive Interview"],
        "roadmap": {
            "Week 1": "Advanced SQL optimization, multi-table indexing, CTEs, and window partition functions.",
            "Week 2": "Python Core: Pandas dataframes, NumPy operations, and pipeline data cleansing methodologies.",
            "Week 3": "BI Dashboard Architecture: Star schemas, relational modeling, DAX parameters, and LOD calculations.",
            "Week 4": "Statistical Modeling: Probability distributions, A/B testing frameworks, and executive stakeholder presentation strategies.",
            "projects": ["Global E-Commerce Interactive Revenue Dashboard", "Algorithmic Logistics Disruption Predictive Insights Model"],
            "certs": ["Google Data Analytics Professional Certificate", "Microsoft Certified: Power BI Data Analyst Associate"],
            "books": ["'Storytelling with Data' by Cole Nussbaumer Knaflic", "'Python for Data Analysis' by Wes McKinney"],
            "courses": ["Coursera: Advanced SQL for Data Science", "edX: Data Analysis Foundations"],
            "playlists": ["Alex The Analyst Data Engineering Pathway", "StatQuest Behavioral Data Science Matrix"]
        },
        "company_intel": {
            "overview": "Focuses intensely on scalable data structures, analytical processing velocity, and dashboard storytelling clarity.",
            "hiring_pattern": "Heavy focus on continuous technical take-home SQL/Dashboard assignments prior to live loops.",
            "salary": "$85,000 - $140,000 base range based on level entry.",
            "difficulty": "Medium to High",
            "q_sql": "Write a query to calculate the 7-day rolling average of user transaction volume.",
            "q_excel": "Explain how to safely deploy an INDEX-MATCH matrix versus an expensive VLOOKUP across 1M rows.",
            "q_stats": "What is a p-value, and how do you prevent alpha error inflation during multi-variant testing?",
            "q_python": "How do you detect and safely impute missing values in a highly skewed dataset using Pandas?",
            "q_behavioral": "Describe a scenario where your analytical results contradicted a Product Manager's core assumption. How did you handle it?",
            "q_hr": "Why choose data analytics at this company over engineering or direct product tracks?",
            "q_tech": "Explain the architectural difference between a data warehouse and a data lake house.",
            "q_case": "Revenue dropped 12% week-over-week for a delivery application. Walk me through your diagnostics framework."
        }
    },
    "📈 Financial Analyst": {
        "companies": ["Goldman Sachs", "JPMorgan Chase", "Morgan Stanley", "BlackRock", "Citi", "HSBC", "American Express", "Deloitte", "EY", "KPMG"],
        "skills": ["Financial Modelling", "Excel", "Accounting", "Corporate Finance", "Valuation", "Forecasting", "Financial Statements", "Power BI"],
        "rounds": ["Aptitude Assessment", "Finance Technical Matrix", "Timed Excel Modeling Test", "Strategic Case Study", "HR Executive Panel"],
        "roadmap": {
            "Week 1": "Advanced corporate accounting mechanics and structural line-item matching across Three-Statement financial modules.",
            "Week 2": "Discounted Cash Flow (DCF) architecture, WACC optimization calculations, and enterprise terminal growth assumptions.",
            "Week 3": "Market Multiples: Public Comps, Precedent Transactions, and capital structure normalization analysis.",
            "Week 4": "Advanced Scenario Forecasting: Monte Carlo sensitivity tables, debt schedule building, and management deck production.",
            "projects": ["Full 3-Statement Dynamic Valuation Module for an Enterprise SaaS Entity", "Leveraged Buyout (LBO) Leveraged Capital Optimization Model"],
            "certs": ["FMVA (Financial Modeling & Valuation Analyst)", "CFA Investment Foundations Program"],
            "books": ["'Investment Banking' by Rosenbaum & Pearl", "'Corporate Finance' by Jonathan Berk"],
            "courses": ["Wall Street Prep: Premium Corporate Valuation Suite", "Coursera: Financial Markets by Yale University"],
            "playlists": ["Corporate Finance Institute Core Path", "Mergers & Inquisitions Analysis Vault"]
        },
        "company_intel": {
            "overview": "Requires absolute precision in regulatory financial statement parsing and rigorous economic logic frameworks.",
            "hiring_pattern": "Strict 3-hour live modeling case tests followed by fast-paced technical testing loops.",
            "salary": "$95,000 - $160,000 base range + standard performance bonus.",
            "difficulty": "High",
            "q_sql": "How can database schema indexing optimize multi-year portfolio ledger calculations?",
            "q_excel": "Walk through building a programmatic dynamic sensitivity table utilizing data tables in Excel.",
            "q_stats": "How do you leverage standard deviation calculations to map portfolio value-at-risk (VaR)?",
            "q_python": "Write a Python snippet to convert regular company cash flow lists into present values using a discount rate array.",
            "q_behavioral": "Tell me about a time you found a significant formula error in a model right before a client presentation.",
            "q_hr": "How do you manage extreme deadlines and high-pressure deliverables typical of financial tracking intervals?",
            "q_tech": "If Depreciation increases by $10, walk me through how it trickles down the 3 financial statements.",
            "q_case": "A consumer brand client wants to expand operations into Western Europe. Evaluate the capital expenditure viability."
        }
    },
    "💼 Business Analyst": {
        "companies": ["Accenture", "Deloitte", "Capgemini", "Infosys", "TCS", "Cognizant", "IBM", "Microsoft", "Amazon", "PwC"],
        "skills": ["SQL", "Excel", "Power BI", "Tableau", "Business Process Mapping", "Agile Frameworks", "Jira Architecture", "Requirement Gathering", "Data Analysis"],
        "rounds": ["Aptitude Testing", "Business Case Structure Evaluation", "SQL Fundamentals", "Excel Analysis Test", "HR Behavioral Fit Loop"],
        "roadmap": {
            "Week 1": "Agile software delivery patterns, writing enterprise user epics, and engineering clear acceptance criteria.",
            "Week 2": "Business Process Model and Notation (BPMN) design, current-state vs future-state workflow gap analysis.",
            "Week 3": "Product Backlog Grooming, prioritization matrix architecture (MoSCoW, RICE score calculations), and Jira setup.",
            "Week 4": "Stakeholder mapping, structural technical documentation delivery, and data-backed ROI business case generation.",
            "projects": ["Enterprise CRM Transformation Product Blueprint & Functional Requirements Document", "Supply Chain Operational Waste Minimization Case Study"],
            "certs": ["CBAP (Certified Business Analysis Professional)", "PMI-PBA (Professional in Business Analysis)"],
            "books": ["'Business Analysis Body of Knowledge (BABOK Guide)'", "'Inspired' by Marty Cagan"],
            "courses": ["Udemy: Business Analysis Process Masterclass", "LinkedIn Learning: Enterprise Requirements Gathering"],
            "playlists": ["Bridging the Gap: Business Analyst Career Track", "BA Mentor Workflow Mapping Solutions"]
        },
        "company_intel": {
            "overview": "Bridges the translation layer between high-level management objectives and low-level software engineering blueprints.",
            "hiring_pattern": "Heavy validation of whiteboard workflow modeling, functional scenario logic mapping, and structured systems thinking.",
            "salary": "$80,000 - $135,000 base metrics.",
            "difficulty": "Medium",
            "q_sql": "Draft a relational query joining customer conversion tables with technical product feature flags.",
            "q_excel": "How do you implement conditional formatting parameters to track performance delays in operational metrics?",
            "q_stats": "How does statistical sampling help gather representative user feedback metrics for a system upgrade?",
            "q_python": "How would you parse an unstructured JSON configuration script into a tabular system requirements list via Pandas?",
            "q_behavioral": "How do you navigate a situation where engineering leaders tell you a critical business feature is technically unviable?",
            "q_hr": "What is your philosophy on resolving conflicting feature priorities between competing business departments?",
            "q_tech": "Explain the architectural difference between a functional requirement and a non-functional requirement.",
            "q_case": "An insurance provider wants to reduce their manual claim processing lifecycle from 14 days down to 48 hours. Map the execution path."
        }
    },
    "📉 Investment Analyst": {
        "companies": ["BlackRock", "Morgan Stanley", "Goldman Sachs", "JP Morgan", "UBS", "Fidelity", "Morningstar", "Barclays", "HSBC", "Nomura"],
        "skills": ["Equity Research", "Portfolio Analysis", "Financial Modelling", "Valuation Matrices", "Bloomberg Terminal Processing", "Excel Engines", "Financial Markets Theory"],
        "rounds": ["Core Finance Concepts Screening", "Valuation Modeling Sprint", "Global Markets Presentation Loop", "Investment Thesis Defense Case", "HR Executive Fit Assessment"],
        "roadmap": {
            "Week 1": "Macroeconomic framework parsing, yield curve dynamics, Federal Reserve balance sheet movements, and capital asset pricing model (CAPM) dynamics.",
            "Week 2": "Microeconomic corporate tracking: competitive moat mapping, Michael Porter's Five Forces framework, and earnings call transcript forensic mapping.",
            "Week 3": "Advanced capital allocation structuring: tracking share buyback programs, enterprise debt refinancing risks, and corporate dividend safety profiles.",
            "Week 4": "Investment thesis production: writing research reports, building investment slide pitches, and defending valuations against cross-examination models.",
            "projects": ["Long/Short Equity Investment Thesis on a Megacap Technology Entity", "Macro Asset Allocation Portfolio Backtesting & Optimization Module"],
            "certs": ["CFA Charterholder Track (Level 1/2/3 Preparation)", "Bloomberg Market Concepts (BMC) License"],
            "books": ["'The Intelligent Investor' by Benjamin Graham", "'Margin of Safety' by Seth Klarman"],
            "courses": ["Coursera: Portfolio Management Foundations", "Wharton: Asset Pricing Masterclass"],
            "playlists": ["Damodaran Valuation Class Archive", "Bloomberg Global Markets Live Streams Analysis"]
        },
        "company_intel": {
            "overview": "Requires deep understanding of market trends, sector fundamentals, and risk-return optimization profiles.",
            "hiring_pattern": "Candidates must deliver an investment recommendation report and defend it in front of an investment committee panel.",
            "salary": "$110,000 - $190,000 base starting configurations (plus performance allocation bonuses).",
            "difficulty": "Very High",
            "q_sql": "How do you extract pricing variables from transactional time-series data using structured window arrays?",
            "q_excel": "How do you structure custom portfolio optimization models utilizing the iterative Excel Solver engine?",
            "q_stats": "Explain the application of Alpha, Beta, and the Sharpe Ratio when reviewing a fund manager's historical returns.",
            "q_python": "Write a script utilizing `yfinance` to extract moving average metrics across an entire index ticker list.",
            "q_behavioral": "Tell me about a market trend you accurately called that went against general consensus, or a time you lost capital on an assumption.",
            "q_hr": "Why choose active asset allocation management over passive algorithmic index systems?",
            "q_tech": "Explain the structural mechanics of a Credit Default Swap (CDS) and its systemic pricing impacts.",
            "q_case": "A legacy automotive company announces a complete transition to solid-state EV batteries. Evaluate its risk profile as a debt investor."
        }
    },
    "💰 Finance Analyst": {
        "companies": ["Amazon", "Google", "Microsoft", "Apple", "Deloitte", "EY", "KPMG", "PwC", "Oracle", "Intel"],
        "skills": ["Financial Reporting", "Budgeting Matrix", "Forecasting Engines", "Power BI Portals", "Excel Core", "SAP Architecture", "SQL Databases", "Corporate Accounting"],
        "rounds": ["Finance Technical Evaluation", "Excel Accounting Challenge", "SQL Query Matching", "Business Scenario Planning Simulation", "HR Cultural Fit Assessment"],
        "roadmap": {
            "Week 1": "Corporate Budgeting frameworks: traditional incremental models vs zero-based budgeting (ZBB) platform migrations.",
            "Week 2": "Variance Analysis mechanics: calculating price, volume, mix, and structural efficiency variations across large sales sheets.",
            "Week 3": "Operating Expenses (OpEx) tracking, Capital Expenditures (CapEx) control loops, and multi-department headcount planning pipelines.",
            "Week 4": "Rolling Forecast architecture: syncing software tooling inputs (SAP, Oracle Hyperion) with dynamic rolling prediction engines.",
            "projects": ["Global Enterprise OpEx Variance Mitigation System Portfolio", "Multi-Department 12-Month Dynamic Headcount Financial Runway Model"],
            "certs": ["CMA (Certified Management Accountant)", "FPAC (Financial Planning & Analysis Certified)"],
            "books": ["'Financial Planning & Analysis and Performance Management' by Jack Alexander", "'Accounting Game' by Darrell Mullis"],
            "courses": ["LinkedIn Learning: Corporate FP&A Foundations", "Udemy: SAP Financial Accounting Essentials"],
            "playlists": ["The FP&A Guy: Corporate Finance Guidance", "Anaplan Financial Modeling Workflows"]
        },
        "company_intel": {
            "overview": "Manages internal corporate runways, expense tracking, and strategic asset optimization paths.",
            "hiring_pattern": "Focuses heavily on identifying operational cost variations and matching real-world engineering costs with high-level corporate revenue.",
            "salary": "$85,000 - $145,000 range parameters.",
            "difficulty": "Medium to High",
            "q_sql": "Draft a multi-table join aggregate grouping operational expenses by corporate ledger division id.",
            "q_excel": "How do you use SUMIFS and nested logic to generate dynamic monthly spending forecasts based on changing category flags?",
            "q_stats": "How can you leverage linear regression models to predict next quarter's production overhead expenses?",
            "q_python": "How do you automate sending automated alerts when a department spends past 90% of its budget using standard scripts?",
            "q_behavioral": "Describe a scenario where you had to push a senior leader to cut their operational budget by 15% due to wider corporate targets.",
            "q_hr": "What is your approach to handling sudden, unexpected regulatory cash flow requirements at the end of a fiscal year?",
            "q_tech": "Explain the difference between Accrual Accounting and Cash Basis Accounting and why corporations rely on the former.",
            "q_case": "Our cloud computing infrastructure costs spiked 35% this quarter, outstripping target projections. Structure an optimization plan."
        }
    }
}

# Initialize State Arrays safely to hold session data
if "eval_results" not in st.session_state:
    st.session_state.eval_results = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==========================================
# 3. GLOBAL NAVIGATION MATRIX
# ==========================================
with st.sidebar:
    st.markdown("<div style='text-align: center; padding: 10px 0;'><h2 style='color:#6366f1; margin:0;'>NEXUS ANALYST AI</h2><p style='color:#6b7280; font-size:11px;'>ENTERPRISE SUITE v3.5</p></div>", unsafe_allow_html=True)
    
    st.markdown("### 🛠️ Configuration Workspace")
    target_role = st.selectbox("Target Analytical Role", list(ROLE_DATA.keys()))
    
    # Contextual dropdown mapping based on selected role
    available_companies = ROLE_DATA[target_role]["companies"]
    target_company = st.selectbox("Target Dream Company", available_companies)
    
    exp_level = st.selectbox("Experience Tier", ["Entry-Level / Graduate", "Associate / Mid-Market", "Senior Staff / Principal Leader"])
    interview_type = st.selectbox("Assessment Target", ["Comprehensive Assessment Loop", "Technical Only Sprint", "Executive Leadership & HR Alignment"])
    
    st.markdown("---")
    menu_selection = st.radio(
        "Application Navigation Grid",
        ["🎯 Performance Practice Dashboard", "🗺️ Personalized Learning Roadmap", "🏢 Company Deep Dive Intelligence", "🎤 Dynamic AI Mock Interview Space", "📚 Curated Resource Vault", "💬 Specialist AI Career Coach"]
    )
    
    st.markdown("---")
    st.markdown("<span class='badge-vip'>✨ ENTERPRISE LEVEL PRO PACK SAVED</span>", unsafe_allow_html=True)

# Fetch data snapshot for active role selections
role_snapshot = ROLE_DATA[target_role]

# ==========================================
# FEATURE 1: PRACTICE DASHBOARD
# ==========================================
if menu_selection == "🎯 Performance Practice Dashboard":
    st.title("🎯 Platform Interactive Practice Dashboard")
    st.subheader(f"Tracking Profile Integration: {target_role} @ {target_company}")
    
    # Metric Grid
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='kpi-container'><div class='kpi-title'>Target Architecture</div><div class='kpi-value' style='font-size:16px; height:32px; padding-top:8px;'>{target_company}</div><div class='kpi-sub' style='color:#6366f1;'>Role: {target_role.split()[-1]}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='kpi-container'><div class='kpi-title'>Skills Mastered</div><div class='kpi-value'>6 / 8</div><div class='kpi-sub'>↑ 2 added this week</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='kpi-container'><div class='kpi-title'>Problems Resolved</div><div class='kpi-value'>42 Questions</div><div class='kpi-sub'>Top 8% of applicants</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='kpi-container'><div class='kpi-title'>Mock Assessments</div><div class='kpi-value'>7 Sessions</div><div class='kpi-sub' style='color:#a855f7;'>3 Verified Tracks</div></div>", unsafe_allow_html=True)

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.markdown("<div class='kpi-container'><div class='kpi-title'>Readiness Score</div><div class='kpi-value' style='color:#10b981;'>88%</div><div class='kpi-sub'>Target Company Clear Vector</div></div>", unsafe_allow_html=True)
    with col6:
        st.markdown("<div class='kpi-container'><div class='kpi-title'>Weekly Delta Progress</div><div class='kpi-value'>+14.3%</div><div class='kpi-sub'>Continuous Optimization</div></div>", unsafe_allow_html=True)
    with col7:
        st.markdown("<div class='kpi-container'><div class='kpi-title'>Practice Streak</div><div class='kpi-value' style='color:#ef4444;'>18 Days 🔥</div><div class='kpi-sub'>Keep momentum active</div></div>", unsafe_allow_html=True)
    with col8:
        st.markdown("<div class='kpi-container'><div class='kpi-title'>Peer Leaderboard Rank</div><div class='kpi-value'>#142</div><div class='kpi-sub'>Global Enterprise Pool</div></div>", unsafe_allow_html=True)

    st.markdown("### 📊 Interactive Operational Metrics")
    chart_a, chart_b = st.columns([2, 1])
    
    with chart_a:
        st.write("#### Historical Skill Domain Progress Trend")
        skill_tracking_data = pd.DataFrame({
            'Week 1 Progress': [40, 30, 20, 50, 60],
            'Week 2 Progress': [55, 45, 38, 62, 75],
            'Week 3 Progress': [75, 68, 55, 80, 88],
            'Week 4 (Current)': [90, 85, 78, 92, 91]
        }, index=role_snapshot["skills"][:5])
        st.line_chart(skill_tracking_data.T)
        
    with chart_b:
        st.write("#### Topic Performance Vector")
        topic_metrics = pd.DataFrame({
            "Core Competency": ["Technical SQL/Accounting", "Case Analysis", "Dashboard UX / Modeling", "Communication", "Behavioral Frameworks"],
            "Score %": [92, 78, 85, 89, 94]
        })
        st.bar_chart(topic_metrics.set_index("Core Competency"))

# ==========================================
# FEATURE 2: PERSONALIZED ROADMAP
# ==========================================
elif menu_selection == "🗺️ Personalized Learning Roadmap":
    st.title("🗺️ AI Adaptive Learning Roadmap Matrix")
    st.caption(f"Optimized Path for {target_role} profile framework.")
    
    st.markdown("### 🛠️ Core Skill Competency Distribution Requirements")
    cols = st.columns(len(role_snapshot["skills"]))
    for idx, skill in enumerate(role_snapshot["skills"]):
        cols[idx].info(f"**{skill}**")
        
    st.markdown("---")
    st.markdown("### 📅 High-Velocity 4-Week Strategic Preparation Framework")
    
    for week in ["Week 1", "Week 2", "Week 3", "Week 4"]:
        with st.expander(f"🚀 {week}: Strategy & Focus Area Analysis", expanded=True):
            st.write(role_snapshot["roadmap"][week])
            st.caption("Action Items: Complete 5 corresponding system practice questions below to unlock next structural tracking loop.")

    st.markdown("---")
    st.markdown("### 📦 Recommended Portfolio Projects & Certifications")
    p_col, c_col = st.columns(2)
    with p_col:
        st.markdown("<div class='section-card'><h4>💼 Production Portfolio Blueprints</h4>", unsafe_allow_html=True)
        for proj in role_snapshot["roadmap"]["projects"]:
            st.markdown(f"* **{proj}**")
        st.markdown("</div>", unsafe_allow_html=True)
    with c_col:
        st.markdown("<div class='section-card'><h4>📜 Verified Industry Certifications</h4>", unsafe_allow_html=True)
        for cert in role_snapshot["roadmap"]["certs"]:
            st.markdown(f"* **{cert}**")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# FEATURE 3: COMPANY INTELLIGENCE
# ==========================================
elif menu_selection == "🏢 Company Deep Dive Intelligence":
    st.title(f"🏢 Company Intel Portal: {target_company}")
    st.subheader(f"Targeting Operational Frameworks for {target_role}")
    
    col_x, col_y, col_z = st.columns(3)
    col_x.metric("Target Assessment Complexity", role_snapshot["company_intel"]["difficulty"])
    col_y.metric("Expected Base Market Compensation", role_snapshot["company_intel"]["salary"])
    col_z.metric("Historical Selection Conversion Rate", "3.4% Matrix Scale")
    
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown(f"#### 🌐 Strategic Company Overview")
    st.write(role_snapshot["company_intel"]["overview"])
    st.markdown(f"#### 🎯 Internal Hiring & Evaluation Blueprint")
    st.write(role_snapshot["company_intel"]["hiring_pattern"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### 📋 Scheduled Interview Loops Matrix")
    for step_idx, step in enumerate(role_snapshot["rounds"]):
        st.markdown(f"**Stage {step_idx + 1}:** {step}")

# ==========================================
# FEATURE 4: AI MOCK INTERVIEW
# ==========================================
elif menu_selection == "🎤 Dynamic AI Mock Interview Space":
    st.title(f"🎤 {target_company} Dedicated AI Mock Assessment Loop")
    st.write("Select a generated company assessment question category below to test your technical syntax and communication parameters.")
    
    question_bank = [
        {"cat": "1. SQL Query Logic Block", "text": role_snapshot["company_intel"]["q_sql"]},
        {"cat": "2. Excel Operational Matrix", "text": role_snapshot["company_intel"]["q_excel"]},
        {"cat": "3. Statistical Analysis Vector", "text": role_snapshot["company_intel"]["q_stats"]},
        {"cat": "4. Python Pipeline Implementation", "text": role_snapshot["company_intel"]["q_python"]},
        {"cat": "5. Strategic System Case Study", "text": role_snapshot["company_intel"]["q_case"]},
        {"cat": "6. Core Domain Technical Concept", "text": role_snapshot["company_intel"]["q_tech"]},
        {"cat": "7. STAR Behavioral Leadership", "text": role_snapshot["company_intel"]["q_behavioral"]},
        {"cat": "8. Cultural Fit & Executive HR Alignment", "text": role_snapshot["company_intel"]["q_hr"]}
    ]
    
    for idx, q in enumerate(question_bank):
        with st.expander(f"❓ Category Vector - {q['cat']}", expanded=(idx == 0)):
            st.markdown(f"<div style='background:rgba(255,255,255,0.02); padding:15px; border-radius:8px; margin-bottom:10px; border-left:4px solid #6366f1;'><strong>Interviewer Prompt:</strong> {q['text']}</div>", unsafe_allow_html=True)
            
            user_ans = st.text_area("Input your complete technical/conceptual structural response:", key=f"ans_block_{idx}", height=120)
            
            if st.button("Submit Response and Execute Assessment Analysis", key=f"btn_{idx}"):
                if not user_ans.strip():
                    st.warning("Please input structured response parameters before triggering validation metrics.")
                else:
                    with st.spinner("Processing structural tokens via evaluation matrices..."):
                        time.sleep(1.2)
                        
                        # Generate realistic multi-dimensional analytics scores based on response length heuristics
                        base_score = min(9.4, max(4.5, 5.0 + (len(user_ans) / 120.0) + random.uniform(-0.5, 0.5)))
                        comm_score = min(10.0, max(5.0, base_score + random.uniform(-0.4, 0.6)))
                        gram_score = random.choice([8.0, 9.0, 9.5, 10.0])
                        conf_score = min(10.0, max(4.0, base_score + random.uniform(-0.8, 0.4)))
                        
                        st.session_state.eval_results[idx] = {
                            "score": round(base_score, 1),
                            "comm": round(comm_score, 1),
                            "gram": round(gram_score, 1),
                            "conf": round(conf_score, 1)
                        }
                        
            # Render evaluation panels if data exists inside Session State
            if idx in st.session_state.eval_results:
                res = st.session_state.eval_results[idx]
                st.markdown("#### 📊 Evaluation Matrix Output Feedback")
                
                sc1, sc2, sc3, sc4 = st.columns(4)
                sc1.metric("Target Vector Score", f"{res['score']} / 10")
                sc2.metric("Communication Clarity", f"{res['comm']} / 10")
                sc3.metric("Syntactic/Grammar Score", f"{res['gram']} / 10")
                sc4.metric("Calculated Confidence Matrix", f"{res['conf']} / 10")
                
                st.markdown("""
                <div style='background:rgba(16,185,129,0.05); padding:15px; border-radius:8px; border:1px solid rgba(16,185,129,0.2); margin-top:10px;'>
                    <span style='color:#10b981; font-weight:700;'>🎯 Target Reference Ideal Response Blueprint:</span><br/>
                    • Establish clear framework structure parameters up-front.<br/>
                    • Explicitly state data structures or financial equations utilized (e.g., matching keys, partition schemas, or DCF discounting variables).<br/>
                    • Conclude with a real-world strategic business execution outcome metrics impact point.
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style='background:rgba(239,68,68,0.05); padding:15px; border-radius:8px; border:1px solid rgba(239,68,68,0.2); margin-top:10px;'>
                    <span style='color:#ef4444; font-weight:700;'>🚨 Detected Missing Vectors & Improvement Steps:</span><br/>
                    • Expand execution detailing inside the practical scenario steps.<br/>
                    • Inject deeper quantitative terminology to eliminate generic phrasing filler structures.<br/>
                    • Ensure structural compliance maps cleanly to the required {exp_level} engineering expectation framework.
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# FEATURE 5: CURATED RESOURCE VAULT
# ==========================================
elif menu_selection == "📚 Curated Resource Vault":
    st.title("📚 Highly Curated Strategic Domain Resource Vault")
    st.write(f"Vetted educational tracks mapping directly to the **{target_role}** skill pipeline requirements.")
    
    v1, v2, v3 = st.columns(3)
    with v1:
        st.markdown("<div class='section-card'><h4>📚 Core Domain Literature</h4>", unsafe_allow_html=True)
        for book in role_snapshot["roadmap"]["books"]:
            st.markdown(f"* {book}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with v2:
        st.markdown("<div class='section-card'><h4>📺 Screen-Targeted Playlists</h4>", unsafe_allow_html=True)
        for playlist in role_snapshot["roadmap"]["playlists"]:
            st.markdown(f"* {playlist}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with v3:
        st.markdown("<div class='section-card'><h4>🌐 Open-Source Learning Accelerators</h4>", unsafe_allow_html=True)
        for course in role_snapshot["roadmap"]["courses"]:
            st.markdown(f"* {course}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 🛠️ Universal Career Readiness Templates")
    t1, t2, t3 = st.columns(3)
    t1.download_button("📥 Download Premium ATS Resume Template", "ATS Clean Formatting Data Block", "ATS_Resume_Template.txt")
    t2.download_button("📥 Download Executive Cover Letter Blueprint", "Cover Letter Dynamic Matrix Text", "Cover_Letter_Blueprint.txt")
    t3.download_button("📥 Download Technical Interview Cheat Sheet", "Core Cheat Sheet Optimization Text Reference", "Technical_Cheat_Sheet.txt")

# ==========================================
# FEATURE 6: SPECIALIST AI CAREER COACH
# ==========================================
elif menu_selection == "💬 Specialist AI Career Coach":
    st.title("💬 Nexus Core AI Domain Career Coach Workspace")
    st.write("Interact with an AI assistant initialized with dedicated functional context parameters matching your selected role track.")
    
    # Render quick prompt assistance macros
    st.markdown("##### ⚡ Quick Prompt Engineering Macros")
    macro_cols = st.columns(4)
    pm1 = macro_cols[0].button("Explain Advanced SQL Partitioning Concepts")
    pm2 = macro_cols[1].button("Explain Structural Financial Valuation Models")
    pm3 = macro_cols[2].button("Explain Core BI Star Schema Design Mechanics")
    pm4 = macro_cols[3].button("Generate Cover Letter Framework Draft")
    
    # Catch quick prompt macros selections
    injected_prompt = ""
    if pm1: injected_prompt = "Explain advanced SQL window partitioning functions and performance optimization patterns with example data blocks."
    if pm2: injected_prompt = "Walk me through the foundational calculations and core theory behind financial valuation modeling and DCF structures."
    if pm3: injected_prompt = "What is the structural difference between a star schema and a snowflake schema in Power BI and Tableau visualization models?"
    if pm4: injected_prompt = f"Draft an executive corporate cover letter outline targeted at {target_company} for a {target_role} profile track."
    
    # Historic Chat Container Rendering Loops
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Process user query or macro selection inputs
    user_query = st.chat_input("Input custom queries here (e.g., 'Optimize my resume bullet points for Stripe', 'Explain accounting')...")
    active_prompt = user_query if user_query else (injected_prompt if injected_prompt else None)
    
    if active_prompt:
        if not user_query:
            st.session_state.chat_history.append({"role": "user", "content": active_prompt})
            with st.chat_message("user"):
                st.markdown(active_prompt)
                
        if user_query:
            st.session_state.chat_history.append({"role": "user", "content": active_prompt})
            with st.chat_message("user"):
                st.markdown(active_prompt)
                
        with st.chat_message("assistant"):
            response_container = st.empty()
            simulated_response = ""
            
            base_coach_responses = [
                f"Processing system logic context parameters for {target_role}... To stand out at {target_company}, ensure your core code snippets or scenario metrics highlight scalable design architectures, processing volume metrics, and explicit business conversions. Let's optimize this strategy line by line.",
                f"Analyzing requested parameters... When explaining these concepts in an interview loop at {target_company}, always structure your answers around cross-functional data pipelines, quantitative variance mitigations, and specific tooling architectures (like advanced Python matrices, clean SQL constraints, or complex financial models)."
            ]
            
            selected_response_base = random.choice(base_coach_responses)
            full_context_text = f"**[Nexus Coach System Response Mode Activated]**\n\n{selected_response_base}\n\nHere is your requested guidance breakdown:\n\n1. Ensure complete structural compliance with the target evaluation rubrics.\n2. Leverage quantitative outcome data metrics throughout your descriptions.\n3. Keep your explanation frameworks linear and conversational."
            
            # Simulate high-end model output streaming effects
            for chunk in full_context_text.split(" "):
                simulated_response += chunk + " "
                time.sleep(0.04)
                response_container.markdown(simulated_response + "▌")
            response_container.markdown(simulated_response)
            
        st.session_state.chat_history.append({"role": "assistant", "content": simulated_response})
