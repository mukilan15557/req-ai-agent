import streamlit as st
import time
import json
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
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Global ---------- */

    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(99,102,241,0.16), transparent 28%),
            radial-gradient(circle at 90% 10%, rgba(168,85,247,0.12), transparent 25%),
            #080b12;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        background: #0b0f18;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* ---------- Headings ---------- */

    h1 {
        font-size: 3.2rem !important;
        font-weight: 800 !important;
        letter-spacing: -2px;
    }

    h2 {
        font-weight: 750 !important;
    }

    h3 {
        font-weight: 700 !important;
    }

    /* ---------- Hero ---------- */

    .hero-box {
        padding: 2rem;
        border-radius: 24px;
        background: linear-gradient(
            135deg,
            rgba(99,102,241,0.22),
            rgba(168,85,247,0.12)
        );
        border: 1px solid rgba(255,255,255,0.10);
        margin-bottom: 1.5rem;
    }

    .hero-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: rgba(99,102,241,0.18);
        border: 1px solid rgba(129,140,248,0.35);
        font-size: 0.82rem;
        font-weight: 700;
        color: #c7d2fe;
        margin-bottom: 12px;
    }

    .hero-title {
        font-size: 2.7rem;
        font-weight: 850;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #aab2c0;
        max-width: 850px;
        line-height: 1.6;
    }

    /* ---------- Cards ---------- */

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 16px;
        padding: 16px;
    }

    div[data-testid="stMetricValue"] {
        font-weight: 800;
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        border-radius: 12px;
        min-height: 46px;
        font-weight: 700;
        border: 1px solid rgba(255,255,255,0.10);
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        border-color: rgba(129,140,248,0.6);
    }

    /* ---------- Text Area ---------- */

    textarea {
        border-radius: 14px !important;
    }

    /* ---------- Tabs ---------- */

    button[data-baseweb="tab"] {
        font-weight: 700;
    }

    /* ---------- Expander ---------- */

    details {
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        background: rgba(255,255,255,0.025) !important;
    }

    /* ---------- Divider ---------- */

    hr {
        border-color: rgba(255,255,255,0.08);
    }

    /* ---------- Footer ---------- */

    .footer {
        text-align: center;
        color: #747d8c;
        font-size: 0.85rem;
        padding-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero-box">
        <div class="hero-badge">G14 • AI REQUIREMENTS ENGINEERING AGENT</div>
        <div class="hero-title">🚀 ReqPilot</div>
        <div class="hero-subtitle">
            Transform raw project ideas into structured software requirements,
            Agile user stories, feature priorities, ambiguity detection,
            test cases and technical dependencies.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🚀 ReqPilot")

    st.caption("AI Requirements Engineering Agent")

    st.divider()

    st.subheader("⚙️ Agent Settings")

    api_key = st.secrets.get("GEMINI_API_KEY", "")

    if api_key:
        st.success("🟢 Gemini API Connected")
    else:
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="Enter API key"
        )

    st.divider()

    st.subheader("💡 Demo Presets")

    preset = st.selectbox(
        "Choose an example",
        [
            "Custom Idea",
            "College Attendance System",
            "AI Cold Outreach Platform",
            "EV Charging Network",
            "Student Learning Platform"
        ]
    )

    st.divider()

    st.subheader("🧠 AI Pipeline")

    st.write("🔍 Requirement Extraction")
    st.write("🏷️ Requirement Classification")
    st.write("🎯 Feature Prioritization")
    st.write("⚠️ Ambiguity Detection")
    st.write("👤 User Story Generation")
    st.write("🧪 Test Case Generation")

    st.divider()

    st.caption("Built for 24-Hour Hackathon")
    st.caption("Python • Streamlit • Gemini")


# ============================================================
# SAMPLE PROJECTS
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

default_input = sample_pitches.get(preset, "")


# ============================================================
# PROJECT INPUT
# ============================================================

st.header("💡 Describe Your Project")

st.caption(
    "Start with a raw idea, problem statement or incomplete project notes."
)

startup_pitch = st.text_area(
    "Project Idea",
    value=default_input,
    height=170,
    placeholder=(
        "Example: We want to build an attendance system "
        "for colleges..."
    ),
    label_visibility="collapsed"
)


# ============================================================
# INPUT STATS
# ============================================================

word_count = len(startup_pitch.split())

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
        "📦 Artifacts",
        "6"
    )

with col4:
    st.metric(
        "⚡ Engine",
        "Gemini"
    )


# ============================================================
# PIPELINE
# ============================================================

st.subheader("🔄 Requirement Intelligence Pipeline")

pipeline = [
    ("💡", "Raw Idea"),
    ("🔍", "Extract"),
    ("🏷️", "Classify"),
    ("🎯", "Prioritize"),
    ("⚠️", "Detect Gaps"),
    ("🧪", "Generate Tests")
]

pipeline_cols = st.columns(6)

for col, item in zip(pipeline_cols, pipeline):

    with col:

        icon, name = item

        with st.container(border=True):

            st.markdown(
                f"### {icon}"
            )

            st.caption(name)


# ============================================================
# ACTION BUTTONS
# ============================================================

st.divider()

button_col1, button_col2, button_col3 = st.columns(
    [3, 1, 1]
)

with button_col1:

    generate_btn = st.button(
        "⚡ Analyze Requirements",
        type="primary",
        use_container_width=True
    )

with button_col2:

    demo_btn = st.button(
        "🎬 Demo Mode",
        use_container_width=True
    )

with button_col3:

    clear_btn = st.button(
        "🗑️ Clear",
        use_container_width=True
    )


# ============================================================
# CLEAR
# ============================================================

if clear_btn:

    st.rerun()


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
            "scenario": "Teacher submits attendance successfully.",
            "expected_result":
                "Attendance records are saved and reflected in student dashboards."
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
# RESULT DISPLAY
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

    st.header("📊 Requirement Intelligence")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "📋 Requirements",
            len(functional) + len(non_functional)
        )

    with m2:
        st.metric(
            "👤 User Stories",
            len(stories)
        )

    with m3:
        st.metric(
            "🧪 Test Cases",
            len(test_cases)
        )

    with m4:
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

        st.subheader("Functional Requirements")

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

            with st.expander(
                f"User Story {i} • "
                f"{story.get('priority', 'Not specified')}",
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
                    f"**Expected:** "
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
        "📥 Export"
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
        "🎬 Demo Mode — using prepared requirement analysis."
    )

    display_results(
        demo_data
    )


# ============================================================
# GEMINI GENERATION
# ============================================================

elif generate_btn:

    if not api_key:

        st.error(
            "❌ Gemini API key is not configured."
        )

    elif not startup_pitch.strip():

        st.warning(
            "⚠️ Please enter a project idea."
        )

    else:

        client = genai.Client(
            api_key=api_key
        )


        prompt = f"""
You are an expert AI Requirements Engineering Agent.

Analyze this software project idea:

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

Requirements:

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


                    # 429
                    if "429" in error_message:

                        st.error(
                            "🚫 Gemini API quota exceeded."
                        )

                        st.info(
                            "Use 🎬 Demo Mode for the hackathon demo "
                            "without consuming another API request."
                        )

                        break


                    # 503
                    elif "503" in error_message:

                        if attempt < 2:

                            wait_time = 2 ** attempt

                            st.warning(
                                f"⚠️ Gemini is busy. "
                                f"Retrying in {wait_time}s..."
                            )

                            time.sleep(
                                wait_time
                            )

                        else:

                            st.error(
                                "❌ Gemini is temporarily unavailable."
                            )


                    # Other errors
                    else:

                        st.error(
                            f"❌ Execution Error: {e}"
                        )

                        break


        # ====================================================
        # PARSE RESPONSE
        # ====================================================

        if response is not None:

            try:

                result_text = response.text.strip()

                # Remove markdown fences if Gemini adds them
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
                    "⚠️ Could not parse the AI response."
                )

                st.code(
                    response.text,
                    language="text"
                )

                st.caption(
                    f"Parser error: {e}"
                )


# ============================================================
# LANDING SECTION
# ============================================================

if not generate_btn and not demo_btn:

    st.divider()

    st.header(
        "✨ From Idea → Development-Ready Requirements"
    )

    st.caption(
        "One raw project idea can generate multiple useful engineering artifacts."
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        with st.container(border=True):

            st.subheader(
                "📋 Requirement Extraction"
            )

            st.write(
                "Convert informal ideas into clear "
                "functional and non-functional requirements."
            )

    with c2:

        with st.container(border=True):

            st.subheader(
                "⚠️ Gap Detection"
            )

            st.write(
                "Identify missing information and "
                "generate clarification questions."
            )

    with c3:

        with st.container(border=True):

            st.subheader(
                "🧪 Test Generation"
            )

            st.write(
                "Create practical test cases from "
                "the generated requirements."
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        ReqPilot • G14 AI Requirements Engineering Agent<br>
        Built with Python + Streamlit + Generative AI
    </div>
    """,
    unsafe_allow_html=True
)
