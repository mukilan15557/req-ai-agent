import streamlit as st
import json
import time
from google import genai
from google.genai import types


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ReqPilot | AI Requirements Engineering",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LIQUID GLASS UI
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL BACKGROUND
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(99, 102, 241, 0.20),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(56, 189, 248, 0.16),
                transparent 28%
            ),
            radial-gradient(
                circle at 50% 90%,
                rgba(168, 85, 247, 0.14),
                transparent 30%
            ),
            #070910;
        color: #f5f7ff;
    }


    /* ======================================================
       MAIN CONTAINER
       ====================================================== */

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                rgba(16, 20, 34, 0.94),
                rgba(8, 11, 20, 0.96)
            );

        border-right: 1px solid rgba(255,255,255,0.10);

        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
    }


    section[data-testid="stSidebar"] * {
        color: #eef2ff;
    }


    /* ======================================================
       HERO GLASS
       ====================================================== */

    .liquid-hero {

        position: relative;

        padding: 42px;

        border-radius: 30px;

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.12),
                rgba(255,255,255,0.035)
            );

        border: 1px solid rgba(255,255,255,0.16);

        box-shadow:
            0 25px 80px rgba(0,0,0,0.35),
            inset 0 1px 1px rgba(255,255,255,0.18);

        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);

        overflow: hidden;

        margin-bottom: 28px;
    }


    .liquid-hero::before {

        content: "";

        position: absolute;

        width: 260px;
        height: 260px;

        right: -80px;
        top: -100px;

        background:
            radial-gradient(
                circle,
                rgba(129,140,248,0.32),
                transparent 70%
            );

        filter: blur(12px);
    }


    .liquid-hero::after {

        content: "";

        position: absolute;

        width: 220px;
        height: 220px;

        left: -100px;
        bottom: -120px;

        background:
            radial-gradient(
                circle,
                rgba(56,189,248,0.18),
                transparent 70%
            );

        filter: blur(15px);
    }


    .hero-content {
        position: relative;
        z-index: 2;
    }


    .hero-badge {

        display: inline-block;

        padding: 7px 14px;

        border-radius: 999px;

        background:
            rgba(129,140,248,0.13);

        border:
            1px solid rgba(165,180,252,0.28);

        color: #c7d2fe;

        font-size: 0.78rem;

        font-weight: 750;

        letter-spacing: 0.5px;

        margin-bottom: 16px;
    }


    .hero-title {

        font-size: 3.4rem;

        line-height: 1.05;

        font-weight: 850;

        letter-spacing: -2.5px;

        margin-bottom: 15px;

        background:
            linear-gradient(
                100deg,
                #ffffff,
                #c7d2fe,
                #bae6fd
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    .hero-subtitle {

        color: #aeb8cb;

        font-size: 1.08rem;

        line-height: 1.7;

        max-width: 850px;
    }


    /* ======================================================
       GLASS CARDS
       ====================================================== */

    .glass-card {

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.085),
                rgba(255,255,255,0.025)
            );

        border:
            1px solid rgba(255,255,255,0.12);

        border-radius: 22px;

        padding: 24px;

        box-shadow:
            0 18px 50px rgba(0,0,0,0.20),
            inset 0 1px 1px rgba(255,255,255,0.08);

        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);

        transition:
            transform 0.25s ease,
            border-color 0.25s ease,
            box-shadow 0.25s ease;
    }


    .glass-card:hover {

        transform: translateY(-3px);

        border-color:
            rgba(165,180,252,0.28);

        box-shadow:
            0 22px 60px rgba(0,0,0,0.30),
            0 0 30px rgba(99,102,241,0.08);
    }


    /* ======================================================
       METRICS
       ====================================================== */

    div[data-testid="stMetric"] {

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.085),
                rgba(255,255,255,0.025)
            );

        border:
            1px solid rgba(255,255,255,0.11);

        border-radius: 20px;

        padding: 18px;

        box-shadow:
            inset 0 1px 1px rgba(255,255,255,0.07),
            0 12px 35px rgba(0,0,0,0.18);

        backdrop-filter: blur(22px);
        -webkit-backdrop-filter: blur(22px);
    }


    div[data-testid="stMetricLabel"] {
        color: #9da8bb !important;
    }


    div[data-testid="stMetricValue"] {
        font-weight: 800;
        color: #f8fafc !important;
    }


    /* ======================================================
       INPUT
       ====================================================== */

    div[data-baseweb="textarea"] {

        background:
            rgba(255,255,255,0.035);

        border-radius: 18px;

        border:
            1px solid rgba(255,255,255,0.12);

        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }


    textarea {

        color: #f8fafc !important;

        font-size: 1rem !important;

        line-height: 1.6 !important;
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {

        border-radius: 15px;

        min-height: 48px;

        font-weight: 750;

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.10),
                rgba(255,255,255,0.045)
            );

        border:
            1px solid rgba(255,255,255,0.14);

        color: #f8fafc;

        box-shadow:
            0 8px 25px rgba(0,0,0,0.18),
            inset 0 1px 1px rgba(255,255,255,0.10);

        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);

        transition: all 0.22s ease;
    }


    .stButton > button:hover {

        transform: translateY(-2px);

        border-color:
            rgba(165,180,252,0.40);

        box-shadow:
            0 12px 35px rgba(99,102,241,0.18);
    }


    /* Primary button */

    button[kind="primary"] {

        background:
            linear-gradient(
                135deg,
                #6366f1,
                #8b5cf6
            ) !important;

        border:
            1px solid rgba(255,255,255,0.25) !important;

        box-shadow:
            0 10px 35px rgba(99,102,241,0.30),
            inset 0 1px 1px rgba(255,255,255,0.25) !important;
    }


    /* ======================================================
       TABS
       ====================================================== */

    button[data-baseweb="tab"] {

        font-weight: 700;

        color: #9ca8bc;
    }


    button[data-baseweb="tab"][aria-selected="true"] {

        color: #ffffff !important;
    }


    div[data-baseweb="tab-highlight"] {

        background:
            linear-gradient(
                90deg,
                #6366f1,
                #a855f7
            );
    }


    /* ======================================================
       EXPANDERS
       ====================================================== */

    details {

        background:
            rgba(255,255,255,0.035) !important;

        border:
            1px solid rgba(255,255,255,0.10) !important;

        border-radius: 16px !important;

        backdrop-filter: blur(20px);
    }


    /* ======================================================
       ALERTS
       ====================================================== */

    div[data-testid="stAlert"] {

        border-radius: 16px;

        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }


    /* ======================================================
       PIPELINE
       ====================================================== */

    .pipeline-card {

        text-align: center;

        padding: 22px 12px;

        border-radius: 18px;

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.075),
                rgba(255,255,255,0.025)
            );

        border:
            1px solid rgba(255,255,255,0.10);

        box-shadow:
            inset 0 1px 1px rgba(255,255,255,0.08);

        backdrop-filter: blur(20px);

        transition: 0.25s ease;
    }


    .pipeline-card:hover {

        transform: translateY(-4px);

        border-color:
            rgba(129,140,248,0.35);
    }


    .pipeline-icon {

        font-size: 1.7rem;

        margin-bottom: 7px;
    }


    .pipeline-name {

        color: #dce3ef;

        font-size: 0.85rem;

        font-weight: 700;
    }


    /* ======================================================
       SECTION TITLES
       ====================================================== */

    .section-kicker {

        color: #818cf8;

        font-size: 0.78rem;

        font-weight: 800;

        letter-spacing: 1.5px;

        text-transform: uppercase;

        margin-bottom: 4px;
    }


    /* ======================================================
       FEATURE CARDS
       ====================================================== */

    .feature-title {

        font-size: 1.1rem;

        font-weight: 750;

        color: #f1f5f9;

        margin-bottom: 8px;
    }


    .feature-text {

        color: #9da8ba;

        line-height: 1.55;

        font-size: 0.92rem;
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {

        text-align: center;

        color: #667085;

        font-size: 0.82rem;

        padding-top: 35px;

        line-height: 1.7;
    }


    /* ======================================================
       DIVIDER
       ====================================================== */

    hr {

        border-color:
            rgba(255,255,255,0.08) !important;

        margin-top: 28px !important;
        margin-bottom: 28px !important;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🚀 ReqPilot")

    st.caption(
        "AI Requirements Engineering Agent"
    )

    st.divider()

    st.markdown("### ⚙️ Agent Control")

    api_key = st.secrets.get(
        "GEMINI_API_KEY",
        ""
    )

    if api_key:

        st.success(
            "🟢 Gemini Connected"
        )

    else:

        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="Paste API key..."
        )

    st.divider()

    st.markdown("### 💡 Demo Presets")

    preset = st.selectbox(
        "Choose a project",
        [
            "Custom Idea",
            "College Attendance System",
            "AI Cold Outreach Platform",
            "EV Charging Network",
            "Student Learning Platform"
        ]
    )

    st.divider()

    st.markdown("### 🧠 AI Pipeline")

    st.write("🔍 Requirement Extraction")
    st.write("🏷️ Classification")
    st.write("🎯 Prioritization")
    st.write("⚠️ Gap Detection")
    st.write("👤 User Stories")
    st.write("🧪 Test Cases")

    st.divider()

    st.caption(
        "G14 • 24-Hour Hackathon"
    )

    st.caption(
        "Python + Streamlit + Gemini"
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="liquid-hero">
        <div class="hero-content">

            <div class="hero-badge">
                G14 • AI REQUIREMENTS ENGINEERING AGENT
            </div>

            <div class="hero-title">
                🚀 ReqPilot
            </div>

            <div class="hero-subtitle">
                Transform raw project ideas into structured software
                requirements, Agile user stories, priorities,
                ambiguity detection and development-ready test cases.
            </div>

        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SAMPLE INPUTS
# ============================================================

sample_pitches = {

    "College Attendance System":
        "We want to build a college attendance management system "
        "where teachers can mark attendance and students can view "
        "their attendance. Students should receive alerts when "
        "their attendance is low.",

    "AI Cold Outreach Platform":
        "We want an AI platform for freelance developers where users "
        "can upload their portfolio, generate personalized outreach "
        "messages, track responses and manage potential clients.",

    "EV Charging Network":
        "We want a platform where homeowners with EV chargers can "
        "allow nearby electric vehicle drivers to book charging slots "
        "and make payments securely.",

    "Student Learning Platform":
        "We want an AI-powered learning platform where students can "
        "upload study material, ask questions, receive explanations "
        "and track their learning progress."
}

default_input = sample_pitches.get(
    preset,
    ""
)


# ============================================================
# PROJECT INPUT
# ============================================================

st.markdown(
    '<div class="section-kicker">INPUT</div>',
    unsafe_allow_html=True
)

st.header(
    "💡 Describe Your Project"
)

st.caption(
    "Start with a raw idea, problem statement or incomplete project notes."
)

startup_pitch = st.text_area(
    "Project Idea",
    value=default_input,
    height=175,
    placeholder=(
        "Example: We want to build an AI-powered "
        "college attendance system..."
    ),
    label_visibility="collapsed"
)


# ============================================================
# METRICS
# ============================================================

word_count = len(
    startup_pitch.split()
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "📝 Input Words",
        word_count
    )

with col2:

    st.metric(
        "🧠 AI Modules",
        "6"
    )

with col3:

    st.metric(
        "📦 Output Artifacts",
        "6"
    )

with col4:

    st.metric(
        "⚡ AI Engine",
        "Gemini"
    )


# ============================================================
# PIPELINE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-kicker">INTELLIGENCE PIPELINE</div>',
    unsafe_allow_html=True
)

st.header(
    "🔄 From Raw Idea → Engineering Artifacts"
)

pipeline = [

    ("💡", "Raw Idea"),

    ("🔍", "Extract"),

    ("🏷️", "Classify"),

    ("🎯", "Prioritize"),

    ("⚠️", "Detect Gaps"),

    ("🧪", "Test Cases")
]


pipeline_cols = st.columns(6)

for col, item in zip(
    pipeline_cols,
    pipeline
):

    icon, name = item

    with col:

        st.markdown(
            f"""
            <div class="pipeline-card">

                <div class="pipeline-icon">
                    {icon}
                </div>

                <div class="pipeline-name">
                    {name}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# ACTIONS
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

action1, action2 = st.columns(
    [3, 1]
)

with action1:

    generate_btn = st.button(
        "⚡ Analyze Requirements",
        type="primary",
        use_container_width=True
    )

with action2:

    demo_btn = st.button(
        "🎬 Demo Mode",
        use_container_width=True
    )


# ============================================================
# DEMO DATA
# ============================================================

demo_data = {

    "functional_requirements": [

        "Teachers must be able to mark attendance for students.",

        "Students must be able to view their attendance percentage.",

        "The system must automatically calculate attendance.",

        "Students must receive alerts when attendance falls below "
        "the configured threshold."
    ],

    "non_functional_requirements": [

        "The system should provide secure role-based access.",

        "Attendance records should be stored reliably.",

        "The dashboard should provide acceptable response time."
    ],

    "user_stories": [

        {
            "story":
                "As a teacher, I want to mark attendance for my class "
                "so that student attendance records remain up to date.",

            "priority":
                "Must Have",

            "acceptance_criteria": [

                "Given a teacher is logged in, when attendance is "
                "submitted, then the attendance record should be saved.",

                "Given attendance submission fails, when the teacher "
                "retries, then the system should display an error."
            ]
        },

        {
            "story":
                "As a student, I want to view my attendance percentage "
                "so that I can monitor my attendance status.",

            "priority":
                "Must Have",

            "acceptance_criteria": [

                "Given attendance records exist, when the student "
                "opens the dashboard, then the current percentage "
                "should be displayed.",

                "Given attendance data is unavailable, when the dashboard "
                "loads, then the system should display an appropriate message."
            ]
        }
    ],

    "priorities": [

        {
            "feature": "Teacher Attendance Entry",
            "priority": "Must Have",
            "reason": "Core functionality of the attendance system."
        },

        {
            "feature": "Student Attendance Dashboard",
            "priority": "Must Have",
            "reason": "Students need to monitor attendance."
        },

        {
            "feature": "Low Attendance Alerts",
            "priority": "Should Have",
            "reason": "Provides proactive notifications."
        }
    ],

    "ambiguities": [

        {
            "issue":
                "The low attendance threshold is not specified.",

            "question":
                "Should the threshold be configurable by the institution?"
        },

        {
            "issue":
                "The notification channel is not specified.",

            "question":
                "Should alerts use email, SMS or in-app notifications?"
        }
    ],

    "test_cases": [

        {
            "id": "TC-01",

            "scenario":
                "Teacher submits attendance successfully.",

            "expected_result":
                "Attendance records are saved and reflected in "
                "student dashboards."
        },

        {
            "id": "TC-02",

            "scenario":
                "Student attendance falls below the threshold.",

            "expected_result":
                "The student receives a low-attendance notification."
        },

        {
            "id": "TC-03",

            "scenario":
                "Unauthorized user attempts to modify attendance.",

            "expected_result":
                "The system denies the operation."
        }
    ],

    "technical_dependencies": [

        "Role-based authentication",

        "Relational database",

        "Notification service",

        "REST API layer",

        "Streamlit frontend"
    ]
}


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(data):

    functional = data.get(
        "functional_requirements",
        []
    )

    non_functional = data.get(
        "non_functional_requirements",
        []
    )

    stories = data.get(
        "user_stories",
        []
    )

    priorities = data.get(
        "priorities",
        []
    )

    ambiguities = data.get(
        "ambiguities",
        []
    )

    test_cases = data.get(
        "test_cases",
        []
    )

    dependencies = data.get(
        "technical_dependencies",
        []
    )


    # ========================================================
    # RESULTS HEADER
    # ========================================================

    st.divider()

    st.markdown(
        '<div class="section-kicker">AI OUTPUT</div>',
        unsafe_allow_html=True
    )

    st.header(
        "📊 Requirement Intelligence"
    )


    # ========================================================
    # RESULT METRICS
    # ========================================================

    r1, r2, r3, r4 = st.columns(4)

    with r1:

        st.metric(
            "📋 Requirements",
            len(functional) + len(non_functional)
        )

    with r2:

        st.metric(
            "👤 User Stories",
            len(stories)
        )

    with r3:

        st.metric(
            "🧪 Test Cases",
            len(test_cases)
        )

    with r4:

        st.metric(
            "⚠️ Gaps",
            len(ambiguities)
        )


    # ========================================================
    # TABS
    # ========================================================

    tabs = st.tabs(
        [
            "📋 Requirements",
            "👤 User Stories",
            "🎯 Priorities",
            "⚠️ Gaps",
            "🧪 Test Cases",
            "🏗️ Technical"
        ]
    )


    # ========================================================
    # REQUIREMENTS
    # ========================================================

    with tabs[0]:

        st.subheader(
            "Functional Requirements"
        )

        for i, requirement in enumerate(
            functional,
            1
        ):

            with st.container(border=True):

                st.markdown(
                    f"**FR-{i:02d}**"
                )

                st.write(
                    requirement
                )


        st.subheader(
            "Non-Functional Requirements"
        )

        for i, requirement in enumerate(
            non_functional,
            1
        ):

            with st.container(border=True):

                st.markdown(
                    f"**NFR-{i:02d}**"
                )

                st.write(
                    requirement
                )


    # ========================================================
    # USER STORIES
    # ========================================================

    with tabs[1]:

        st.subheader(
            "👤 Agile User Stories"
        )

        for i, story in enumerate(
            stories,
            1
        ):

            priority = story.get(
                "priority",
                "Not specified"
            )

            with st.expander(
                f"User Story {i} • {priority}",
                expanded=True
            ):

                st.write(
                    story.get(
                        "story",
                        ""
                    )
                )

                st.markdown(
                    "#### ✅ Acceptance Criteria"
                )

                for criterion in story.get(
                    "acceptance_criteria",
                    []
                ):

                    st.write(
                        f"✓ {criterion}"
                    )


    # ========================================================
    # PRIORITIES
    # ========================================================

    with tabs[2]:

        st.subheader(
            "🎯 Feature Prioritization"
        )

        for item in priorities:

            with st.container(border=True):

                st.markdown(
                    f"### {item.get('feature', 'Feature')}"
                )

                st.write(
                    f"**Priority:** "
                    f"{item.get('priority', 'Not specified')}"
                )

                st.caption(
                    item.get(
                        "reason",
                        ""
                    )
                )


    # ========================================================
    # GAPS
    # ========================================================

    with tabs[3]:

        st.subheader(
            "⚠️ Missing & Ambiguous Requirements"
        )

        if ambiguities:

            for issue in ambiguities:

                with st.container(border=True):

                    st.warning(
                        issue.get(
                            "issue",
                            ""
                        )
                    )

                    st.write(
                        "💬 "
                        + issue.get(
                            "question",
                            ""
                        )
                    )

        else:

            st.success(
                "✅ No major ambiguities detected."
            )


    # ========================================================
    # TEST CASES
    # ========================================================

    with tabs[4]:

        st.subheader(
            "🧪 Generated Test Cases"
        )

        for test in test_cases:

            with st.container(border=True):

                st.markdown(
                    f"### {test.get('id', 'TC')}"
                )

                st.write(
                    f"**Scenario:** "
                    f"{test.get('scenario', '')}"
                )

                st.write(
                    f"**Expected Result:** "
                    f"{test.get('expected_result', '')}"
                )


    # ========================================================
    # TECHNICAL
    # ========================================================

    with tabs[5]:

        st.subheader(
            "🏗️ Technical Dependencies"
        )

        for dependency in dependencies:

            st.write(
                f"🔹 {dependency}"
            )


    # ========================================================
    # EXPORT
    # ========================================================

    st.divider()

    st.subheader(
        "📥 Export Requirements"
    )

    json_data = json.dumps(
        data,
        indent=4,
        ensure_ascii=False
    )

    st.download_button(
        "📥 Download Requirements JSON",
        data=json_data,
        file_name="ReqPilot_Requirements.json",
        mime="application/json",
        use_container_width=True
    )


# ============================================================
# DEMO MODE
# ============================================================

if demo_btn:

    st.success(
        "🎬 Demo Mode activated — using prepared analysis."
    )

    display_results(
        demo_data
    )


# ============================================================
# GEMINI AI
# ============================================================

elif generate_btn:

    if not api_key:

        st.error(
            "❌ Gemini API key is not configured."
        )

    elif not startup_pitch.strip():

        st.warning(
            "⚠️ Please enter a project idea first."
        )

    else:

        client = genai.Client(
            api_key=api_key
        )


        prompt = f"""
You are an expert AI Requirements Engineering Agent.

Analyze the following software project idea:

\"\"\"
{startup_pitch}
\"\"\"

Return ONLY valid JSON.

Use exactly this structure:

{{
    "functional_requirements": [],

    "non_functional_requirements": [],

    "user_stories": [
        {{
            "story": "As a [user], I want to [action], so that [benefit].",
            "priority": "Must Have",
            "acceptance_criteria": [
                "Given ... When ... Then ..."
            ]
        }}
    ],

    "priorities": [
        {{
            "feature": "Feature name",
            "priority": "Must Have",
            "reason": "Reason"
        }}
    ],

    "ambiguities": [
        {{
            "issue": "Missing or ambiguous requirement",
            "question": "Clarification question"
        }}
    ],

    "test_cases": [
        {{
            "id": "TC-01",
            "scenario": "Test scenario",
            "expected_result": "Expected result"
        }}
    ],

    "technical_dependencies": []
}}

Instructions:

1. Extract functional requirements.
2. Extract non-functional requirements.
3. Generate realistic Agile user stories.
4. Include Given / When / Then acceptance criteria.
5. Prioritize features using Must Have, Should Have and Could Have.
6. Detect missing and ambiguous requirements.
7. Generate practical test cases.
8. Identify technical dependencies.
9. Keep requirements clear and testable.
10. Do not invent unnecessary features.
11. Return ONLY valid JSON.
"""


        response = None

        # ====================================================
        # API REQUEST
        # ====================================================

        with st.spinner(
            "🤖 ReqPilot is analyzing your project..."
        ):

            for attempt in range(3):

                try:

                    response = client.models.generate_content(

                        model="gemini-3.6-flash",

                        contents=prompt,

                        config=types.GenerateContentConfig(
                            response_mime_type="application/json"
                        )
                    )

                    break


                except Exception as e:

                    error_message = str(e)


                    # -------------------------------
                    # 429 QUOTA
                    # -------------------------------

                    if "429" in error_message:

                        st.error(
                            "🚫 Gemini API quota exceeded."
                        )

                        st.info(
                            "Use 🎬 Demo Mode for your hackathon "
                            "presentation without making another API request."
                        )

                        break


                    # -------------------------------
                    # 503 SERVER BUSY
                    # -------------------------------

                    elif "503" in error_message:

                        if attempt < 2:

                            wait_time = 2 ** attempt

                            st.warning(
                                f"⚠️ Gemini is temporarily busy. "
                                f"Retrying in {wait_time}s..."
                            )

                            time.sleep(
                                wait_time
                            )

                        else:

                            st.error(
                                "❌ Gemini is temporarily unavailable."
                            )

                            st.info(
                                "You can use 🎬 Demo Mode to "
                                "show the complete product."
                            )


                    # -------------------------------
                    # OTHER ERROR
                    # -------------------------------

                    else:

                        st.error(
                            f"❌ Execution Error: {e}"
                        )

                        break


        # ====================================================
        # PARSE AI RESPONSE
        # ====================================================

        if response is not None:

            try:

                result_text = response.text.strip()


                # Remove accidental Markdown fences

                if result_text.startswith("```"):

                    result_text = (
                        result_text
                        .replace("```json", "")
                        .replace("```", "")
                        .strip()
                    )


                data = json.loads(
                    result_text
                )


                st.success(
                    "✅ Requirements Generated Successfully!"
                )


                display_results(
                    data
                )


            except Exception as e:

                st.error(
                    "⚠️ The AI response could not be parsed."
                )

                st.code(
                    response.text,
                    language="text"
                )

                st.caption(
                    f"Parser error: {e}"
                )


# ============================================================
# LANDING FEATURES
# ============================================================

if not generate_btn and not demo_btn:

    st.divider()

    st.markdown(
        '<div class="section-kicker">WHY REQPILOT</div>',
        unsafe_allow_html=True
    )

    st.header(
        "✨ Built for Requirements Engineering"
    )

    st.caption(
        "One raw idea → multiple development-ready artifacts."
    )

    f1, f2, f3 = st.columns(3)


    with f1:

        st.markdown(
            """
            <div class="glass-card">

                <div class="feature-title">
                    📋 Requirement Extraction
                </div>

                <div class="feature-text">
                    Converts informal project ideas into
                    structured functional and non-functional
                    requirements.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with f2:

        st.markdown(
            """
            <div class="glass-card">

                <div class="feature-title">
                    ⚠️ Ambiguity Detection
                </div>

                <div class="feature-text">
                    Identifies missing information and creates
                    clarification questions before development begins.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with f3:

        st.markdown(
            """
            <div class="glass-card">

                <div class="feature-title">
                    🧪 Test Generation
                </div>

                <div class="feature-text">
                    Converts requirements into practical
                    test scenarios and expected outcomes.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        <strong>ReqPilot</strong> • G14 AI Requirements Engineering Agent<br>

        Built with Python • Streamlit • Generative AI<br>

        🚀 From raw idea to development-ready requirements

    </div>
    """,
    unsafe_allow_html=True
)
