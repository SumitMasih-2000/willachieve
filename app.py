import streamlit as st
import pandas as pd
import numpy as np
import time
import random

# ==========================================
# 1. PAGE SETUP & STYLE
# ==========================================
st.set_page_config(
    page_title="AI Interview Prep Platform",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, Modern Dark Theme with Smooth Cards
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
    h1, h2, h3, h4 { font-family: 'Inter', sans-serif; font-weight: 600; color: #ffffff; }
    
    /* Simple Premium Cards */
    .metric-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-title { color: #94a3b8; font-size: 14px; margin-bottom: 4px; font-weight: 500; }
    .metric-value { font-size: 28px; font-weight: 700; color: #38bdf8; }
    .metric-sub { font-size: 12px; color: #10b981; margin-top: 2px; }
    
    .card-background {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE MANAGEMENT (TRACKING PROGRESS)
# ==========================================
if "eval_results" not in st.session_state:
    st.session_state.eval_results = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Calculate Dynamic Metrics based on completed questions
questions_solved = len(st.session_state.eval_results)
mock_interviews_completed = 1 if questions_solved > 0 else 0

if questions_solved > 0:
    # Dynamically calculate scores based on user answers
    total_score = sum(res["score"] for res in st.session_state.eval_results.values())
    avg_score = total_score / questions_solved
    readiness_score = min(100, int(avg_score * 10))
    skills_completed = min(8, int(questions_solved * 1.5))
    practice_streak = 1
    weekly_progress = f"+{questions_solved * 12}%"
else:
    # Starting State (Absolute Zero)
    readiness_score = 0
    skills_completed = 0
    practice_streak = 0
    weekly_progress = "0%"

# ==========================================
# 3. ROLE & COMPANY DATA REPOSITORY
# ==========================================
ROLE_DATA = {
    "📊 Data Analyst": {
        "companies": ["Google", "Microsoft", "Amazon", "Deloitte", "Accenture", "PwC", "EY", "KPMG", "TCS", "Infosys"],
        "skills": ["Excel", "SQL", "Python", "Power BI", "Tableau", "Statistics", "Data Cleaning", "Data Visualization"],
        "rounds": ["Resume Screening", "Aptitude Test", "SQL Assessment", "Excel Test", "Python Coding", "Dashboard Case Study", "HR Interview"],
        "roadmap": {
            "Week 1": "Master SQL basics, Joins, Group By, and Aggregations.",
            "Week 2": "Learn Python libraries: Pandas dataframes and NumPy operations.",
            "Week 3": "Build dashboards: Connect data sources, create charts, and format metrics.",
            "Week 4": "Study statistics: A/B testing, distributions, and presenting insights.",
            "projects": ["E-Commerce Revenue Dashboard", "Predictive Logistics Analysis Model"],
            "certs": ["Google Data Analytics Certificate", "Microsoft Power BI Analyst Associate"],
            "books": ["'Storytelling with Data'", "'Python for Data Analysis'"],
            "courses": ["Coursera: SQL for Data Science", "edX: Data Analysis Foundations"],
            "playlists": ["Alex The Analyst Guide", "StatQuest Data Science Channel"]
        },
        "company_intel": {
            "overview": "Focuses on clean data extraction, dashboard design, and translating numbers into business stories.",
            "hiring_pattern": "Requires a take-home SQL or Dashboard assignment followed by a technical interview round.",
            "salary": "$80,000 - $120,000",
            "difficulty": "Medium",
            "q_sql": "Write a query to find the top 5 customers with the highest total order amount this year.",
            "q_excel": "When should you use INDEX-MATCH instead of VLOOKUP, and why?",
            "q_stats": "What is a p-value, and how do you explain it to a non-technical manager?",
            "q_python": "How do you find and replace missing or null values in a Pandas DataFrame?",
            "q_behavioral": "Tell me about a time you found an unexpected insight in a dataset. How did you share it?",
            "q_hr": "Why do you want to work as a Data Analyst at our company?",
            "q_tech": "What is the difference between a Data Warehouse and a Data Lake?",
            "q_case": "Our website sales dropped by 10% last week. How would you investigate the cause?"
        }
    },
    "📈 Financial Analyst": {
        "companies": ["Goldman Sachs", "JPMorgan Chase", "Morgan Stanley", "BlackRock", "Citi", "HSBC", "Deloitte", "EY", "KPMG"],
        "skills": ["Financial Modelling", "Excel", "Accounting", "Corporate Finance", "Valuation", "Forecasting", "Financial Statements", "Power BI"],
        "rounds": ["Aptitude Test", "Finance Technical Interview", "Excel Modeling Test", "Case Study", "HR Interview"],
        "roadmap": {
            "Week 1": "Review basic accounting rules and link the Three Financial Statements.",
            "Week 2": "Build Discounted Cash Flow (DCF) models and calculate WACC.",
            "Week 3": "Learn Valuation multiples: Public Comps and Precedent Transactions.",
            "Week 4": "Practice forecasting: Build revenue models and sensitivity analysis charts.",
            "projects": ["3-Statement Company Valuation Model", "SaaS Business Financial Runway Forecast"],
            "certs": ["FMVA (Financial Modeling Analyst)", "CFA Investment Foundations"],
            "books": ["'Investment Banking' by Rosenbaum", "'Corporate Finance' by Berk"],
            "courses": ["Wall Street Prep: Corporate Valuation", "Coursera: Financial Markets"],
            "playlists": ["Corporate Finance Institute Path", "Mergers & Inquisitions Vault"]
        },
        "company_intel": {
            "overview": "Requires precise accounting logic, financial statement understanding, and high attention to detail.",
            "hiring_pattern": "Includes a timed, 3-hour Excel financial modeling test followed by a technical presentation.",
            "salary": "$90,000 - $140,000",
            "difficulty": "High",
            "q_sql": "How can data indexing improve calculations for a large stock portfolio database?",
            "q_excel": "How do you build a dynamic data table in Excel to test multiple growth scenarios?",
            "q_stats": "How do you calculate standard deviation to measure investment risk?",
            "q_python": "Write a Python script to calculate the future value of a series of cash flows.",
            "q_behavioral": "Describe a time you caught a formula error in a model right before a final deadline.",
            "q_hr": "How do you handle working under tight deadlines and high pressure?",
            "q_tech": "If Depreciation increases by $10, how does it change the three financial statements?",
            "q_case": "A retail client wants to open 50 new stores. How would you analyze if it is a profitable move?"
        }
    },
    "💼 Business Analyst": {
        "companies": ["Accenture", "Deloitte", "Capgemini", "Infosys", "TCS", "Cognizant", "IBM", "Microsoft", "Amazon", "PwC"],
        "skills": ["SQL", "Excel", "Power BI", "Tableau", "Process Mapping", "Agile", "Jira", "Requirement Gathering", "Data Analysis"],
        "rounds": ["Aptitude Test", "Business Case Interview", "SQL Basics", "Excel Test", "HR Interview"],
        "roadmap": {
            "Week 1": "Learn Agile frameworks, writing user stories, and setting acceptance criteria.",
            "Week 2": "Practice workflow mapping (BPMN) and gap analysis.",
            "Week 3": "Master backlog management and feature prioritization techniques (MoSCoW).",
            "Week 4": "Learn requirement gathering techniques and building ROI business cases.",
            "projects": ["CRM Software Upgrade Blueprint", "Supply Chain Cost Optimization Plan"],
            "certs": ["CBAP (Certified Business Analysis Professional)", "PMI-PBA"],
            "books": ["'BABOK Guide'", "'Inspired' by Marty Cagan"],
            "courses": ["Udemy: Business Analysis Masterclass", "LinkedIn Learning: Requirements Gathering"],
            "playlists": ["Bridging the Gap Track", "BA Mentor Workflow Solutions"]
        },
        "company_intel": {
            "overview": "Acts as the bridge between management business goals and software engineering teams.",
            "hiring_pattern": "Focuses on interactive whiteboard sessions where you map out business workflows and resolve operational delays.",
            "salary": "$75,000 - $115,000",
            "difficulty": "Medium",
            "q_sql": "Write a query to connect a user login table with a product feature tracking table.",
            "q_excel": "How do you use conditional formatting to highlight delayed projects in a master list?",
            "q_stats": "How can statistical sampling help you collect user feedback for a software update?",
            "q_python": "How do you convert an unformatted text list into a structured table using Pandas?",
            "q_behavioral": "How do you handle a situation where developers tell you a requested feature is impossible to build?",
            "q_hr": "How do you resolve conflicting product priorities between two different department heads?",
            "q_tech": "What is the difference between a functional requirement and a non-functional requirement?",
            "q_case": "A health insurance company wants to reduce claims processing time from 10 days to 2 days. Walk me through your plan."
        }
    },
    "📉 Investment Analyst": {
        "companies": ["BlackRock", "Morgan Stanley", "Goldman Sachs", "JP Morgan", "UBS", "Fidelity", "Barclays", "HSBC"],
        "skills": ["Equity Research", "Portfolio Analysis", "Financial Modelling", "Valuation", "Bloomberg", "Excel", "Financial Markets"],
        "rounds": ["Finance Core Screening", "Valuation Sprint", "Market Presentation", "Investment Pitch Defense", "HR Interview"],
        "roadmap": {
            "Week 1": "Study macroeconomic trends, interest rates, and yield curves.",
            "Week 2": "Evaluate company competitive moats using Porter's Five Forces.",
            "Week 3": "Analyze corporate actions: stock buybacks, debt refinancing, and dividend health.",
            "Week 4": "Write an investment thesis and prepare a stock pitch presentation deck.",
            "projects": ["Stock Investment Pitch Report", "Historical Portfolio Performance Analysis"],
            "certs": ["CFA Level 1 Candidate", "Bloomberg Market Concepts"],
            "books": ["'The Intelligent Investor'", "'Margin of Safety'"],
            "courses": ["Coursera: Portfolio Management", "Wharton: Asset Pricing Foundations"],
            "playlists": ["Damodaran Valuation Lectures", "Bloomberg Global Markets Feed"]
        },
        "company_intel": {
            "overview": "Requires deep stock market passion, economic understanding, and a logical stock selection process.",
            "hiring_pattern": "Requires submitting a formal stock recommendation report and defending it in front of a committee.",
            "salary": "$100,000 - $160,000",
            "difficulty": "Very High",
            "q_sql": "How do you pull monthly stock price changes out of a transactional database?",
            "q_excel": "Explain how to use the Excel Solver tool to optimize asset allocations in a portfolio.",
            "q_stats": "What are the Sharpe Ratio and Beta coefficient, and why do they matter to an investor?",
            "q_python": "Write a basic script to fetch historical stock data for an index list using an API.",
            "q_behavioral": "Tell me about an investment idea you had that turned out completely wrong. What did you learn?",
            "q_hr": "Why do you want to manage active investments instead of buying passive index funds?",
            "q_tech": "What is a Credit Default Swap, and how does it protect an investor from risk?",
            "q_case": "An automotive company decides to shift 100% of its production to electric vehicles. Is this a good investment? Why?"
        }
    },
    "💰 Finance Analyst": {
        "companies": ["Amazon", "Google", "Microsoft", "Apple", "Deloitte", "EY", "KPMG", "PwC", "Oracle", "Intel"],
        "skills": ["Financial Reporting", "Budgeting", "Forecasting", "Power BI", "Excel", "SAP", "SQL", "Accounting"],
        "rounds": ["Technical Finance Interview", "Excel Accounting Test", "SQL Practice Loop", "Business Scenario Planning", "HR Round"],
        "roadmap": {
            "Week 1": "Learn corporate budgeting methods: Incremental vs Zero-Based budgeting.",
            "Week 2": "Master variance analysis: Find differences between expected budget and actual company spending.",
            "Week 3": "Understand operational expenses (OpEx), capital expenses (CapEx), and team headcount planning.",
            "Week 4": "Learn rolling forecast structures using software tools like SAP or Oracle.",
            "projects": ["Company Operational Cost Variance System", "12-Month Department Budget Model"],
            "certs": ["CMA (Certified Management Accountant)", "FPAC Certification"],
            "books": ["'Financial Planning & Analysis'", "'The Accounting Game'"],
            "courses": ["LinkedIn Learning: FP&A Foundations", "Udemy: SAP Essentials"],
            "playlists": ["The FP&A Guy Channel", "Anaplan Financial Modeling Guides"]
        },
        "company_intel": {
            "overview": "Manages internal corporate cash runways, monitors department spending, and updates company growth forecasts.",
            "hiring_pattern": "Tests your ability to identify corporate overspending patterns and build flexible forecasting solutions.",
            "salary": "$80,000 - $125,000",
            "difficulty": "Medium to High",
            "q_sql": "Write a query to group corporate operational expenses by department ID.",
            "q_excel": "How do you combine SUMIFS and nested logic to track monthly corporate expenses?",
            "q_stats": "How can you use linear regression to predict next quarter's manufacturing costs?",
            "q_python": "How would you automate an email alert when a department exceeds 90% of its budget?",
            "q_behavioral": "How do you handle telling a senior manager that they need to cut their department spending by 10%?",
            "q_hr": "How do you deal with unexpected finance issues or expense updates right at the end of the fiscal year?",
            "q_tech": "What is the difference between Accrual Accounting and Cash Accounting?",
            "q_case": "Our software cloud costs jumped by 30% this quarter. How would you plan a cost-reduction strategy?"
        }
    }
}

# ==========================================
# 4. SIDEBAR CONFIGURATION
# ==========================================
with st.sidebar:
    st.markdown("<div style='text-align: center; padding: 10px 0;'><h2 style='color:#38bdf8; margin:0;'>Prep Dashboard AI</h2><p style='color:#64748b; font-size:12px;'>Student Practice Suite</p></div>", unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Target Settings")
    target_role = st.selectbox("Choose Target Role", list(ROLE_DATA.keys()))
    
    available_companies = ROLE_DATA[target_role]["companies"]
    target_company = st.selectbox("Choose Dream Company", available_companies)
    
    exp_level = st.selectbox("Experience Level", ["Entry-Level / Graduate", "Associate / Mid-Level", "Senior Team Lead"])
    interview_type = st.selectbox("Interview Mode", ["Full Round Loop", "Technical Focus", "HR & Culture Match"])
    
    st.markdown("---")
    menu_selection = st.radio(
        "Navigation",
        ["🎯 Practice Dashboard", "🗺️ Learning Roadmap", "🏢 Company Guide", "🎤 AI Mock Interview", "📚 Study Resources", "💬 AI Career Coach"]
    )

role_snapshot = ROLE_DATA[target_role]

# ==========================================
# PAGE 1: INTERACTIVE DASHBOARD
# ==========================================
if menu_selection == "🎯 Practice Dashboard":
    st.title("🎯 Your Progress Dashboard")
    st.subheader(f"Current Target: {target_role} at {target_company}")
    
    # Live KPI Cards linked to Session State
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-box'><div class='metric-title'>🎯 Target Company</div><div class='metric-value' style='font-size:20px; padding: 4px 0;'>{target_company}</div><div class='metric-sub' style='color:#38bdf8;'>Role: {target_role.split()[-1]}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-box'><div class='metric-title'>💼 Target Role</div><div class='metric-value' style='font-size:20px; padding: 4px 0;'>{target_role.split()[-1]}</div><div class='metric-sub' style='color:#a855f7;'>Tier: {exp_level.split()[0]}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-box'><div class='metric-title'>📚 Skills Completed</div><div class='metric-value'>{skills_completed} / 8</div><div class='metric-sub'>Based on practice</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-box'><div class='metric-title'>📝 Questions Solved</div><div class='metric-value'>{questions_solved} Questions</div><div class='metric-sub'>Across all categories</div></div>", unsafe_allow_html=True)

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.markdown(f"<div class='metric-box'><div class='metric-title'>🎤 Mock Interviews</div><div class='metric-value'>{mock_interviews_completed} Sessions</div><div class='metric-sub'>Completed loops</div></div>", unsafe_allow_html=True)
    with col6:
        st.markdown(f"<div class='metric-box'><div class='metric-title'>⭐ Readiness Score</div><div class='metric-value' style='color:#10b981;'>{readiness_score}%</div><div class='metric-sub'>Target: 85%+ to clear</div></div>", unsafe_allow_html=True)
    with col7:
        st.markdown(f"<div class='metric-box'><div class='metric-title'>📈 Weekly Progress</div><div class='metric-value'>{weekly_progress}</div><div class='metric-sub'>Activity delta</div></div>", unsafe_allow_html=True)
    with col8:
        st.markdown(f"<div class='metric-box'><div class='metric-title'>🔥 Practice Streak</div><div class='metric-value' style='color:#ef4444;'>{practice_streak} Days 🔥</div><div class='metric-sub'>Keep the streak active</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Interactive Performance Analytics")
    
    if questions_solved == 0:
        st.info("💡 **Your progress charts are currently empty.** Go to the **'🎤 AI Mock Interview'** tab in the sidebar, choose a question, and submit your answers to see this dashboard update live!")
    else:
        chart_a, chart_b = st.columns([2, 1])
        with chart_a:
            st.write("#### Skill Progress Over Time")
            # Generate trend data that scales upward with questions solved
            chart_data = pd.DataFrame({
                'Initial Setup': [10, 10, 5, 20, 15],
                'Mid-Week Check': [35, 40, 25, 45, 50],
                'Current Standing': [min(100, 40 + questions_solved*10), min(100, 30 + questions_solved*12), min(100, 20 + questions_solved*15), min(100, 50 + questions_solved*8), min(100, 45 + questions_solved*9)]
            }, index=role_snapshot["skills"][:5])
            st.line_chart(chart_data.T)
            
        with chart_b:
            st.write("#### Topic-wise Performance")
            topic_metrics = pd.DataFrame({
                "Category": ["Technical Mastery", "Case Strategy", "Tooling Syntax", "Clarity", "Behavioral Context"],
                "Score %": [min(100, int(avg_score * 10)), min(100, int(avg_score * 9)), min(100, int(avg_score * 9.5)), min(100, int(avg_score * 10.2)), min(100, int(avg_score * 9.8))]
            })
            st.bar_chart(topic_metrics.set_index("Category"))

# ==========================================
# PAGE 2: LEARNING ROADMAP
# ==========================================
elif menu_selection == "🗺️ Learning Roadmap":
    st.title("🗺️ Your Personalized Learning Roadmap")
    st.caption(f"Curated study timeline to clear requirements for a {target_role} role.")
    
    st.markdown("### 🎯 Required Skills to Master")
    cols = st.columns(len(role_snapshot["skills"]))
    for idx, skill in enumerate(role_snapshot["skills"]):
        cols[idx].info(f"**{skill}**")
        
    st.markdown("---")
    st.markdown("### 📅 Step-by-Step 4-Week Study Plan")
    for week in ["Week 1", "Week 2", "Week 3", "Week 4"]:
        with st.expander(f"🚀 {week} Focus Area", expanded=True):
            st.write(role_snapshot["roadmap"][week])

    st.markdown("---")
    st.markdown("### 📦 Recommended Portfolio Projects & Certifications")
    p_col, c_col = st.columns(2)
    with p_col:
        st.markdown("<div class='card-background'><h4>💼 Recommended Projects</h4>", unsafe_allow_html=True)
        for proj in role_snapshot["roadmap"]["projects"]:
            st.markdown(f"* **{proj}**")
        st.markdown("</div>", unsafe_allow_html=True)
    with c_col:
        st.markdown("<div class='card-background'><h4>📜 Target Certifications</h4>", unsafe_allow_html=True)
        for cert in role_snapshot["roadmap"]["certs"]:
            st.markdown(f"* **{cert}**")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# PAGE 3: COMPANY GUIDE
# ==========================================
elif menu_selection == "🏢 Company Guide":
    st.title(f"🏢 Company Guide: {target_company}")
    
    col_x, col_y, col_z = st.columns(3)
    col_x.metric("Interview Difficulty Level", role_snapshot["company_intel"]["difficulty"])
    col_y.metric("Expected Salary Range", role_snapshot["company_intel"]["salary"])
    col_z.metric("Platform Average Passing Rate", "Top 5% Score Match")
    
    st.markdown("<div class='card-background'>", unsafe_allow_html=True)
    st.markdown(f"#### 🌐 Company Recruitment Focus")
    st.write(role_snapshot["company_intel"]["overview"])
    st.markdown(f"#### 🎯 Interview Process Design")
    st.write(role_snapshot["company_intel"]["hiring_pattern"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### 📋 Scheduled Interview Rounds")
    for step_idx, step in enumerate(role_snapshot["rounds"]):
        st.markdown(f"**Round {step_idx + 1}:** {step}")

# ==========================================
# PAGE 4: AI MOCK INTERVIEW (THE ACTIVE INGREDIENT)
# ==========================================
elif menu_selection == "🎤 AI Mock Interview":
    st.title(f"🎤 {target_company} Practice Session")
    st.write("Answer the company questions below. Your scores will update your central progress dashboard immediately.")
    
    question_list = [
        {"cat": "SQL Practice Question", "text": role_snapshot["company_intel"]["q_sql"]},
        {"cat": "Excel Test Question", "text": role_snapshot["company_intel"]["q_excel"]},
        {"cat": "Statistics Question", "text": role_snapshot["company_intel"]["q_stats"]},
        {"cat": "Python Coding Question", "text": role_snapshot["company_intel"]["q_python"]},
        {"cat": "Business Case Question", "text": role_snapshot["company_intel"]["q_case"]},
        {"cat": "Technical Concept Question", "text": role_snapshot["company_intel"]["q_tech"]},
        {"cat": "Behavioral Question", "text": role_snapshot["company_intel"]["q_behavioral"]},
        {"cat": "HR Round Question", "text": role_snapshot["company_intel"]["q_hr"]}
    ]
    
    for idx, q in enumerate(question_list):
        with st.expander(f"❓ Question Category: {q['cat']}", expanded=(idx == 0)):
            st.markdown(f"<div style='background:rgba(255,255,255,0.02); padding:15px; border-radius:8px; margin-bottom:10px; border-left:4px solid #38bdf8;'><strong>Question:</strong> {q['text']}</div>", unsafe_allow_html=True)
            
            user_ans = st.text_area("Type your complete answer here:", key=f"ans_block_{idx}", height=100)
            
            if st.button("Submit Answer for Grading", key=f"btn_{idx}"):
                if not user_ans.strip():
                    st.warning("Please type an answer before submitting for score analysis.")
                else:
                    with st.spinner("AI evaluating metrics and saving scores..."):
                        time.sleep(1.0)
                        
                        # Generate dynamic scores based on answer depth
                        calculated_base = min(9.8, max(5.0, 5.5 + (len(user_ans) / 100.0) + random.uniform(-0.4, 0.4)))
                        comm_score = min(10.0, max(5.0, calculated_base + random.uniform(-0.2, 0.5)))
                        gram_score = random.choice([8.5, 9.0, 9.5, 10.0])
                        conf_score = min(10.0, max(5.0, calculated_base + random.uniform(-0.5, 0.3)))
                        
                        # Save metrics directly into Session State
                        st.session_state.eval_results[idx] = {
                            "score": round(calculated_base, 1),
                            "comm": round(comm_score, 1),
                            "gram": round(gram_score, 1),
                            "conf": round(conf_score, 1)
                        }
                        st.rerun() # Rerun to update global metrics on the dashboard instantly
                        
            # Show grading report if question has been evaluated
            if idx in st.session_state.eval_results:
                res = st.session_state.eval_results[idx]
                st.markdown("#### 📊 Score Report")
                
                sc1, sc2, sc3, sc4 = st.columns(4)
                sc1.metric("Overall Score", f"{res['score']} / 10")
                sc2.metric("Communication", f"{res['comm']} / 10")
                sc3.metric("Grammar", f"{res['gram']} / 10")
                sc4.metric("Confidence Level", f"{res['conf']} / 10")
                
                st.markdown("""
                <div style='background:rgba(16,185,129,0.05); padding:12px; border-radius:6px; border:1px solid rgba(16,185,129,0.2); margin-top:10px;'>
                    <span style='color:#10b981; font-weight:600;'>💡 Ideal Answer Structure:</span><br/>
                    • State your core choice or equation within the first two sentences.<br/>
                    • Share a clean, structured example (e.g., using CTE layouts or specific variance variables).<br/>
                    • Conclude with the business impact of your decision.
                </div>
                <div style='background:rgba(239,68,68,0.05); padding:12px; border-radius:6px; border:1px solid rgba(239,68,68,0.2); margin-top:10px;'>
                    <span style='color:#ef4444; font-weight:600;'>🔧 Improvement Suggestions:</span><br/>
                    • Avoid generic filler words like 'stuff' or 'things'—use specific analytical terminology.<br/>
                    • Make sure your explanation follows a clear, linear timeline.
                </div>
                """, unsafe_allow_html=True)

# ==========================================
# PAGE 5: CURATED STUDY RESOURCES
# ==========================================
elif menu_selection == "📚 Study Resources":
    st.title("📚 Study Resources & Cheat Sheets")
    st.write(f"Vetted study materials for **{target_role}** roles.")
    
    v1, v2, v3 = st.columns(3)
    with v1:
        st.markdown("<div class='card-background'><h4>📚 Best Books</h4>", unsafe_allow_html=True)
        for book in role_snapshot["roadmap"]["books"]:
            st.markdown(f"* {book}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with v2:
        st.markdown("<div class='card-background'><h4>📺 YouTube Channels</h4>", unsafe_allow_html=True)
        for playlist in role_snapshot["roadmap"]["playlists"]:
            st.markdown(f"* {playlist}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with v3:
        st.markdown("<div class='card-background'><h4>🌐 Free Online Courses</h4>", unsafe_allow_html=True)
        for course in role_snapshot["roadmap"]["courses"]:
            st.markdown(f"* {course}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 🛠️ Placement Templates")
    t1, t2, t3 = st.columns(3)
    t1.download_button("📥 Download Clean ATS Resume Template", "ATS Clean Document Sample Data", "ATS_Resume_Template.txt")
    t2.download_button("📥 Download Cover Letter Guide", "Cover Letter Document Blueprint Text", "Cover_Letter_Guide.txt")
    t3.download_button("📥 Download Interview Cheat Sheet", "Core Interview Cheat Sheet Text", "Technical_Cheat_Sheet.txt")

# ==========================================
# PAGE 6: AI CAREER COACH
# ==========================================
elif menu_selection == "💬 AI Career Coach":
    st.title("💬 AI Career Coach Chatbot")
    st.write("Ask your personal coach questions about technical terms, functions, resumes, or interview questions.")
    
    # Simple Navigation Macros
    st.markdown("##### ⚡ Quick Learning Shortcuts")
    macro_cols = st.columns(4)
    pm1 = macro_cols[0].button("Explain Advanced SQL Functions")
    pm2 = macro_cols[1].button("Explain Financial Valuation Models")
    pm3 = macro_cols[2].button("Explain Business Analytics Star Schemas")
    pm4 = macro_cols[3].button("Generate Cover Letter Framework")
    
    injected_prompt = ""
    if pm1: injected_prompt = "Can you explain how SQL partition functions work with simple table examples?"
    if pm2: injected_prompt = "Walk me through how to build a basic company DCF valuation model step by step."
    if pm3: injected_prompt = "What is a star schema database design, and how is it used in Power BI or Tableau?"
    if pm4: injected_prompt = f"Draft a professional cover letter template targeted at {target_company} for a {target_role} position."
    
    # Display Chat History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Process Inputs
    user_query = st.chat_input("Ask a question about SQL, models, formulas, case studies, or resumes...")
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
            
            coach_text_options = [
                f"Great question! When discussing this concept in an interview loop at {target_company} for a {target_role} role, remember to highlight your understanding of clean pipeline flows, quantitative values, and data tools. Let's look at a clear framework.",
                f"To answer this effectively for a position at {target_company}, break down your logic clearly. Ensure your response targets the specific technical expectations of a {exp_level} role."
            ]
            
            selected_base = random.choice(coach_text_options)
            full_context_text = f"**[AI Coach Engine Response]**\n\n{selected_base}\n\nHere is your step-by-step breakdown:\n\n1. Always organize your technical responses linearly.\n2. Back up your points using data metrics where possible.\n3. Make sure to connect the concept back to the company's daily operations."
            
            # Smooth text streaming effect
            for chunk in full_context_text.split(" "):
                simulated_response += chunk + " "
                time.sleep(0.04)
                response_container.markdown(simulated_response + "▌")
            response_container.markdown(simulated_response)
            
        st.session_state.chat_history.append({"role": "assistant", "content": simulated_response})
