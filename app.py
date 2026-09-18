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
# PROFESSIONAL CSS
# ============================================================

st.markdown("""
<style>

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(59,130,246,0.10), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(139,92,246,0.08), transparent 30%),
        #080b12;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ---------------- HERO ---------------- */

.hero {
    padding: 38px 42px;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.09);
    background: linear-gradient(
        135deg,
        rgba(25,32,52,0.95),
        rgba(13,18,30,0.95)
    );
    box-shadow: 0 20px 60px rgba(0,0,0,0.25);
    margin-bottom: 24px;
}

.badge {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 30px;
    background: rgba(59,130,246,0.14);
    border: 1px solid rgba(59,130,246,0.35);
    color: #8ab4ff;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}

.hero-title {
    font-size: 48px;
    font-weight: 850;
    margin-top: 15px;
    line-height: 1.05;
}

.hero-subtitle {
    color: #a9b3c4;
    font-size: 18px;
    margin-top: 12px;
    max-width: 760px;
    line-height: 1.6;
}


/* ---------------- SECTION ---------------- */

.section-title {
    font-size: 25px;
    font-weight: 750;
    margin-top: 30px;
    margin-bottom: 5px;
}

.section-subtitle {
    color: #8d98aa;
    margin-bottom: 18px;
}


/* ---------------- CARDS ---------------- */

.card {
    background: rgba(18,23,34,0.90);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 17px;
    padding: 22px;
    min-height: 135px;
}

.card-icon {
    font-size: 27px;
}

.card-title {
    font-size: 17px;
    font-weight: 750;
    margin-top: 8px;
}

.card-text {
    color: #8f9aac;
    font-size: 14px;
    line-height: 1.5;
    margin-top: 5px;
}


/* ---------------- METRICS ---------------- */

.metric-card {
    background: linear-gradient(
        145deg,
        rgba(22,29,44,0.95),
        rgba(13,18,28,0.95)
    );
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 18px;
    text-align: center;
}

.metric-number {
    font-size: 30px;
    font-weight: 800;
}

.metric-label {
    color: #8f9aac;
    font-size: 13px;
}


/* ---------------- PIPELINE ---------------- */

.pipeline {
    background: rgba(15,20,30,0.85);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 22px;
    margin: 20px 0;
    text-align: center;
}

.pipeline-step {
    display: inline-block;
    padding: 9px 13px;
    margin: 5px;
    border-radius: 10px;
    background: #171e2d;
    border: 1px solid #2b3549;
    font-size: 13px;
    font-weight: 650;
}

.arrow {
    color: #6d8cff;
    font-weight: 800;
}


/* ---------------- SIDEBAR ---------------- */

section[data-testid="stSidebar"] {
    background: #090d14;
    border-right: 1px solid rgba(255,255,255,0.07);
}


/* ---------------- BUTTONS ---------------- */

.stButton > button {
    border-radius: 11px;
    font-weight: 700;
    min-height: 46px;
}


/* ---------------- TEXT AREA ---------------- */

textarea {
    border-radius: 13px !important;
}


/* ---------------- TABS ---------------- */

.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 9px;
    padding: 9px 13px;
    font-weight: 650;
}


/* ---------------- FOOTER ---------------- */

.footer {
    text-align: center;
    color: #687386;
    font-size: 13px;
    padding-top: 35px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

    <div class="badge">
        G14 • AI REQUIREMENTS ENGINEERING AGENT
    </div>

    <div class="hero-title">
        🚀 ReqPilot
    </div>

    <div class="hero-subtitle">
        Transform raw project ideas into structured software
        requirements, agile user stories, priorities,
        ambiguity detection and test cases.
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ Agent Control")

    api_key = st.secrets.get("GEMINI_API_KEY", "")

    if not api_key:
        api_key = st.text_input(
            "Gemini API Key",
            type="password"
        )
    else:
        st.success("✓ API Key Connected")

    st.markdown("---")

    st.markdown("### 💡 Demo Presets")

    preset = st.selectbox(
        "Select a project",
        [
            "Custom Idea",
            "College Attendance System",
            "AI Cold Outreach Platform",
            "EV Charging Network",
            "Student Learning Platform"
        ]
    )

    st.markdown("---")

    st.markdown("### 🧠 Analysis Pipeline")

    st.caption("01  Requirement Extraction")
    st.caption("02  Classification")
    st.caption("03  Prioritization")
    st.caption("04  Ambiguity Detection")
    st.caption("05  User Stories")
    st.caption("06  Test Generation")

    st.markdown("---")

    st.info(
        "Built for a 24-hour hackathon 🚀"
    )


# ============================================================
# PRESET DATA
# ============================================================

sample_pitches = {

    "College Attendance System":
        """
        We want to build a college attendance management system where
        teachers can mark attendance and students can view their
        attendance. Students should receive alerts when their
        attendance is low.
        """,

    "AI Cold Outreach Platform":
        """
        We want an AI platform for freelance developers where users
        can upload their portfolio, generate personalized outreach
        messages, track responses and manage potential clients.
        """,

    "EV Charging Network":
        """
        We want a platform where homeowners with EV chargers can
        allow nearby electric vehicle drivers to book charging slots
        and make payments securely.
        """,

    "Student Learning Platform":
        """
        We want an AI-powered student learning platform where students
        can upload study material, ask questions, receive personalized
        explanations and track their learning progress.
        """
}

default_input = sample_pitches.get(
    preset,
    ""
)


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown(
    '<div class="section-title">💡 Describe Your Project</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Start with a raw idea, problem statement or incomplete project notes.'
    '</div>',
    unsafe_allow_html=True
)

startup_pitch = st.text_area(
    "Project Idea",
    value=default_input,
    height=175,
    label_visibility="collapsed",
    placeholder=(
        "Example: We want to build an attendance system "
        "where teachers mark attendance..."
    )
)


# ============================================================
# INPUT STATS
# ============================================================

word_count = len(startup_pitch.split())

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-number">{word_count}</div>
            <div class="metric-label">Input Words</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-number">6</div>
            <div class="metric-label">Analysis Modules</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-number">AI</div>
            <div class="metric-label">Requirements Engine</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PIPELINE
# ============================================================

st.markdown("""
<div class="pipeline">

    <span class="pipeline-step">💡 Raw Idea</span>
    <span class="arrow">→</span>

    <span class="pipeline-step">🔍 Extract</span>
    <span class="arrow">→</span>

    <span class="pipeline-step">🎯 Prioritize</span>
    <span class="arrow">→</span>

    <span class="pipeline-step">⚠️ Detect Gaps</span>
    <span class="arrow">→</span>

    <span class="pipeline-step">👤 User Stories</span>
    <span class="arrow">→</span>

    <span class="pipeline-step">🧪 Test Cases</span>

</div>
""", unsafe_allow_html=True)


# ============================================================
# BUTTONS
# ============================================================

col_generate, col_demo = st.columns([3, 1])

with col_generate:
    generate_btn = st.button(
        "⚡ Analyze Requirements",
        type="primary",
        use_container_width=True
    )

with col_demo:
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
        "The system must calculate attendance automatically.",
        "Students must receive alerts when attendance falls below the configured threshold."
    ],

    "non_functional_requirements": [
        "The system should provide secure role-based access.",
        "Attendance records should be stored reliably.",
        "The dashboard should load within an acceptable response time."
    ],

    "user_stories": [
        {
            "story": "As a teacher, I want to mark attendance for my class so that student attendance records remain up to date.",
            "priority": "Must Have",
            "acceptance_criteria": [
                "Given a teacher is logged in, when attendance is submitted, then the attendance record should be saved.",
                "Given attendance submission fails, when the teacher retries, then the system should display an appropriate error."
            ]
        },
        {
            "story": "As a student, I want to view my attendance percentage so that I can monitor my attendance status.",
            "priority": "Must Have",
            "acceptance_criteria": [
                "Given attendance records exist, when the student opens the dashboard, then the current percentage should be displayed.",
                "Given attendance data is unavailable, when the dashboard loads, then the system should display an appropriate message."
            ]
        }
    ],

    "priorities": [
        {
            "feature": "Teacher Attendance Entry",
            "priority": "Must Have",
            "reason": "Core functionality of the system."
        },
        {
            "feature": "Student Attendance Dashboard",
            "priority": "Must Have",
            "reason": "Required for students to monitor attendance."
        },
        {
            "feature": "Low Attendance Alerts",
            "priority": "Should Have",
            "reason": "Provides proactive notification to students."
        }
    ],

    "ambiguities": [
        {
            "issue": "Low attendance threshold is not specified.",
            "question": "Should the threshold be configurable by the institution?"
        },
        {
            "issue": "Notification channel is not specified.",
            "question": "Should alerts use email, SMS or in-app notifications?"
        }
    ],

    "test_cases": [
        {
            "id": "TC-01",
            "scenario": "Teacher submits attendance successfully.",
            "expected_result": "Attendance records are saved and reflected in student dashboards."
        },
        {
            "id": "TC-02",
            "scenario": "Student has attendance below the threshold.",
            "expected_result": "The student receives a low-attendance notification."
        },
        {
            "id": "TC-03",
            "scenario": "Unauthorized user attempts to modify attendance.",
            "expected_result": "The system denies the operation."
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
# FUNCTION TO DISPLAY RESULTS
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
    # RESULT METRICS
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">📊 Requirement Intelligence</div>',
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Requirements",
            len(functional) + len(non_functional)
        )

    with m2:
        st.metric(
            "User Stories",
            len(stories)
        )

    with m3:
        st.metric(
            "Test Cases",
            len(test_cases)
        )

    with m4:
        st.metric(
            "Ambiguities",
            len(ambiguities)
        )


    # ========================================================
    # TABS
    # ========================================================

    tabs = st.tabs([
        "📋 Requirements",
        "👤 User Stories",
        "🎯 Priorities",
        "🧪 Test Cases",
        "⚠️ Gaps & Risks",
        "🏗️ Technical"
    ])


    # ========================================================
    # REQUIREMENTS
    # ========================================================

    with tabs[0]:

        st.subheader("📋 Functional Requirements")

        if functional:

            for i, req in enumerate(
                functional,
                1
            ):
                st.markdown(
                    f"**FR-{i:02d}**  —  {req}"
                )

        else:
            st.info("No functional requirements detected.")


        st.markdown("---")

        st.subheader("⚙️ Non-Functional Requirements")

        if non_functional:

            for i, req in enumerate(
                non_functional,
                1
            ):
                st.markdown(
                    f"**NFR-{i:02d}**  —  {req}"
                )

        else:
            st.info("No non-functional requirements detected.")


    # ========================================================
    # USER STORIES
    # ========================================================

    with tabs[1]:

        st.subheader("👤 Agile User Stories")

        if not stories:
            st.info("No user stories generated.")

        for i, story in enumerate(
            stories,
            1
        ):

            with st.expander(
                f"User Story {i} • {story.get('priority', 'Priority not specified')}",
                expanded=True
            ):

                st.markdown(
                    f"**{story.get('story', '')}**"
                )

                st.markdown(
                    "#### Acceptance Criteria"
                )

                for criterion in story.get(
                    "acceptance_criteria",
                    []
                ):

                    st.markdown(
                        f"✓ {criterion}"
                    )


    # ========================================================
    # PRIORITIES
    # ========================================================

    with tabs[2]:

        st.subheader("🎯 MoSCoW / Feature Prioritization")

        if not priorities:
            st.info("No priorities generated.")

        for item in priorities:

            priority = item.get(
                "priority",
                "Not specified"
            )

            st.markdown(
                f"""
                ### {item.get('feature', 'Feature')}

                **Priority:** `{priority}`

                {item.get('reason', '')}
                """
            )

            st.divider()


    # ========================================================
    # TEST CASES
    # ========================================================

    with tabs[3]:

        st.subheader("🧪 Generated Test Cases")

        if not test_cases:
            st.info("No test cases generated.")

        for test in test_cases:

            st.markdown(
                f"### {test.get('id', 'TC')}"
            )

            st.markdown(
                f"**Scenario:** {test.get('scenario', '')}"
            )

            st.markdown(
                f"**Expected Result:** "
                f"{test.get('expected_result', '')}"
            )

            st.divider()


    # ========================================================
    # AMBIGUITIES
    # ========================================================

    with tabs[4]:

        st.subheader(
            "⚠️ Missing & Ambiguous Requirements"
        )

        if ambiguities:

            for issue in ambiguities:

                st.warning(
                    f"**Gap:** {issue.get('issue', '')}"
                )

                st.info(
                    f"💬 **Clarification:** "
                    f"{issue.get('question', '')}"
                )

        else:

            st.success(
                "✓ No major ambiguities detected."
            )


    # ========================================================
    # TECHNICAL
    # ========================================================

    with tabs[5]:

        st.subheader(
            "🏗️ Technical Dependencies"
        )

        for dependency in dependencies:

            st.markdown(
                f"🔹 {dependency}"
            )


    # ========================================================
    # EXPORT
    # ========================================================

    st.markdown("---")

    st.subheader("📥 Export")

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
        "🎬 Demo Mode activated — no API request used."
    )

    display_results(
        demo_data
    )


# ============================================================
# REAL AI GENERATION
# ============================================================

elif generate_btn:

    if not api_key:

        st.error(
            "❌ Gemini API key is not configured."
        )

    elif not startup_pitch.strip():

        st.warning(
            "⚠️ Enter a project idea first."
        )

    else:

        client = genai.Client(
            api_key=api_key
        )


        # ----------------------------------------------------
        # PROMPT
        # ----------------------------------------------------

        prompt = f"""
You are an expert AI Requirements Engineering Agent.

Analyze the following software project idea:

\"\"\"
{startup_pitch}
\"\"\"

Return ONLY valid JSON using exactly this structure:

{{
    "functional_requirements": [],
    "non_functional_requirements": [],

    "user_stories": [
        {{
            "story": "As a [user], I want to [action], so that [benefit].",
            "priority": "Must Have",
            "acceptance_criteria": []
        }}
    ],

    "priorities": [
        {{
            "feature": "",
            "priority": "Must Have",
            "reason": ""
        }}
    ],

    "ambiguities": [
        {{
            "issue": "",
            "question": ""
        }}
    ],

    "test_cases": [
        {{
            "id": "TC-01",
            "scenario": "",
            "expected_result": ""
        }}
    ],

    "technical_dependencies": []
}}

Requirements:

1. Identify functional requirements.
2. Identify non-functional requirements.
3. Generate realistic Agile user stories.
4. Include Given/When/Then style acceptance criteria.
5. Prioritize features using Must Have, Should Have or Won't Have.
6. Detect missing or ambiguous requirements.
7. Generate practical test cases.
8. Identify important technical dependencies.
9. Do not invent unnecessary features.
10. Return ONLY valid JSON.
"""


        # ----------------------------------------------------
        # GENERATION
        # ----------------------------------------------------

        with st.spinner(
            "🤖 ReqPilot is analyzing your requirements..."
        ):

            response = None

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


                    # 503 = temporary server issue
                    if "503" in error_message:

                        if attempt < 2:

                            wait_time = 2 ** attempt

                            st.warning(
                                f"⚠️ AI service is busy. "
                                f"Retrying in {wait_time}s..."
                            )

                            time.sleep(
                                wait_time
                            )

                        else:

                            st.error(
                                "❌ Gemini is temporarily unavailable. "
                                "Please try again."
                            )


                    # 429 = quota
                    elif "429" in error_message:

                        st.error(
                            "🚫 Gemini API quota has been reached."
                        )

                        st.info(
                            "You can use 🎬 Demo Mode to demonstrate "
                            "the complete frontend without making another API request."
                        )

                        break


                    else:

                        st.error(
                            f"❌ Execution Error: {e}"
                        )

                        break


        # ----------------------------------------------------
        # DISPLAY AI RESULT
        # ----------------------------------------------------

        if response is not None:

            try:

                data = json.loads(
                    response.text
                )

                st.success(
                    "✅ Requirements Successfully Generated!"
                )

                display_results(
                    data
                )

            except Exception as e:

                st.error(
                    "⚠️ The AI response could not be converted into structured data."
                )

                st.code(
                    response.text,
                    language="json"
                )

                st.caption(
                    f"Parsing error: {e}"
                )


# ============================================================
# LANDING FEATURES
# ============================================================

if not generate_btn and not demo_btn:

    st.markdown("---")

    st.markdown(
        '<div class="section-title">✨ Built for Requirements Engineering</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'One raw idea → multiple development-ready artifacts.'
        '</div>',
        unsafe_allow_html=True
    )


    f1, f2, f3 = st.columns(3)


    with f1:

        st.markdown("""
        <div class="card">

            <div class="card-icon">📋</div>

            <div class="card-title">
                Requirement Extraction
            </div>

            <div class="card-text">
                Converts informal project descriptions
                into functional and non-functional requirements.
            </div>

        </div>
        """, unsafe_allow_html=True)


    with f2:

        st.markdown("""
        <div class="card">

            <div class="card-icon">⚠️</div>

            <div class="card-title">
                Ambiguity Detection
            </div>

            <div class="card-text">
                Identifies missing information and generates
                clarification questions before development begins.
            </div>

        </div>
        """, unsafe_allow_html=True)


    with f3:

        st.markdown("""
        <div class="card">

            <div class="card-icon">🧪</div>

            <div class="card-title">
                Test Generation
            </div>

            <div class="card-text">
                Converts requirements into practical test
                scenarios for engineering teams.
            </div>

        </div>
        """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    ReqPilot • AI Requirements Engineering Agent • G14
    <br>
    Built with Python + Streamlit + Generative AI
</div>
""", unsafe_allow_html=True)
