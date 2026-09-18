import streamlit as st
import json
import time
import re

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
# LIQUID GLASS CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(124, 92, 255, 0.18), transparent 30%),
        radial-gradient(circle at 90% 15%, rgba(0, 180, 255, 0.14), transparent 28%),
        radial-gradient(circle at 50% 90%, rgba(180, 70, 255, 0.12), transparent 35%),
        #080b12;
    color: white;
}

/* Main container */
.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            rgba(17, 21, 32, 0.94),
            rgba(8, 11, 18, 0.98)
        );
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: #f5f7ff;
}

/* Glass cards */
.glass {
    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.10),
            rgba(255,255,255,0.035)
        );
    border: 1px solid rgba(255,255,255,0.13);
    border-radius: 24px;
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);
    box-shadow:
        0 20px 60px rgba(0,0,0,0.28),
        inset 0 1px 0 rgba(255,255,255,0.08);
}

/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    padding: 45px 42px;
    margin-bottom: 28px;
    border-radius: 30px;

    background:
        radial-gradient(
            circle at 85% 20%,
            rgba(75, 160, 255, 0.25),
            transparent 30%
        ),
        radial-gradient(
            circle at 15% 80%,
            rgba(150, 80, 255, 0.22),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            rgba(255,255,255,0.11),
            rgba(255,255,255,0.035)
        );

    border: 1px solid rgba(255,255,255,0.15);

    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);

    box-shadow:
        0 25px 80px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.10);
}

.hero:before {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    right: -100px;
    top: -120px;
    border-radius: 50%;
    background: rgba(100,160,255,0.18);
    filter: blur(40px);
}

.hero-badge {
    display: inline-block;
    padding: 8px 15px;
    border-radius: 999px;

    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.14);

    color: #b9c7ff;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.8px;

    margin-bottom: 18px;
}

.hero-title {
    font-size: 58px;
    line-height: 1.05;
    font-weight: 800;
    letter-spacing: -2px;

    background: linear-gradient(
        90deg,
        #ffffff,
        #b9c5ff,
        #9edcff
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-bottom: 16px;
}

.hero-subtitle {
    max-width: 800px;
    color: #b8c0d4;
    font-size: 18px;
    line-height: 1.7;
}

/* Section titles */
.section-label {
    color: #9caeff;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.section-title {
    font-size: 30px;
    font-weight: 800;
    color: white;
    margin-bottom: 22px;
}

/* Metrics */
.metric-card {
    padding: 18px;
    min-height: 105px;

    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.11);
    border-radius: 18px;

    backdrop-filter: blur(18px);
}

.metric-value {
    font-size: 25px;
    font-weight: 800;
    color: white;
}

.metric-label {
    color: #9ca6bb;
    font-size: 12px;
    margin-top: 5px;
}

/* Pipeline */
.pipeline-card {
    min-height: 145px;
    padding: 20px 12px;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.10),
            rgba(255,255,255,0.035)
        );

    border: 1px solid rgba(255,255,255,0.13);
    border-radius: 20px;

    backdrop-filter: blur(18px);

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.08),
        0 15px 35px rgba(0,0,0,0.18);

    transition: transform 0.25s ease;
}

.pipeline-card:hover {
    transform: translateY(-5px);
}

.pipeline-icon {
    font-size: 30px;
    margin-bottom: 12px;
}

.pipeline-title {
    font-weight: 700;
    font-size: 14px;
    color: white;
}

.pipeline-subtitle {
    color: #8f9ab0;
    font-size: 11px;
    margin-top: 5px;
}

/* Feature cards */
.feature-card {
    min-height: 210px;
    padding: 26px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.09),
            rgba(255,255,255,0.035)
        );

    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 24px;

    backdrop-filter: blur(20px);

    box-shadow:
        0 18px 50px rgba(0,0,0,0.20),
        inset 0 1px 0 rgba(255,255,255,0.07);
}

.feature-icon {
    font-size: 27px;
    margin-bottom: 12px;
}

.feature-title {
    font-size: 17px;
    font-weight: 800;
    color: white;
    margin-bottom: 10px;
}

.feature-text {
    color: #9da7ba;
    line-height: 1.6;
    font-size: 13px;
}

/* Input area */
textarea {
    background: rgba(255,255,255,0.055) !important;
    border: 1px solid rgba(255,255,255,0.13) !important;
    border-radius: 18px !important;
    color: white !important;
}

/* Buttons */
.stButton > button {
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.14);

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.10),
            rgba(255,255,255,0.04)
        );

    color: white;
    font-weight: 700;

    min-height: 48px;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.20),
        inset 0 1px 0 rgba(255,255,255,0.08);

    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    border-color: rgba(160,180,255,0.45);
}

/* Primary button */
.stButton > button[kind="primary"] {
    background:
        linear-gradient(
            135deg,
            #7266ff,
            #9a7cff
        );

    border: 1px solid rgba(255,255,255,0.25);

    box-shadow:
        0 12px 40px rgba(110,90,255,0.35);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: rgba(255,255,255,0.035);
    padding: 6px;
    border-radius: 16px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 12px;
    color: #9ba5b9;
}

.stTabs [aria-selected="true"] {
    background: rgba(255,255,255,0.10);
    color: white;
}

/* Expanders */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.045) !important;
    border-radius: 14px !important;
}

/* Footer */
.footer {
    margin-top: 50px;
    padding: 25px;
    text-align: center;

    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.09);

    border-radius: 20px;

    color: #8792a8;
    font-size: 13px;

    backdrop-filter: blur(18px);
}

/* Hide Streamlit menu */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("""
    <div style="
        font-size:28px;
        font-weight:800;
        margin-bottom:4px;
    ">
        🚀 ReqPilot
    </div>

    <div style="
        color:#8f9ab0;
        font-size:13px;
        margin-bottom:25px;
    ">
        AI Requirements Engineering Agent
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔐 AI Connection")

    api_key = None

    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]

            st.success("✓ API Key Connected")

        else:
            api_key = st.text_input(
                "Gemini API Key",
                type="password",
                placeholder="Enter your API key"
            )

    except Exception:
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="Enter your API key"
        )

    st.divider()

    st.markdown("### 🎯 Demo Presets")

    preset = st.selectbox(
        "Choose a sample project",
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

    st.markdown("""
    **01** → Requirement Extraction  
    **02** → Requirement Classification  
    **03** → Priority Analysis  
    **04** → Ambiguity Detection  
    **05** → User Story Generation  
    **06** → Test Case Generation
    """, unsafe_allow_html=True)

    st.divider()

    st.caption("G14 • Hackathon Prototype")


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

    <div class="hero-badge">
        G14 • AI REQUIREMENTS ENGINEERING AGENT
    </div>

    <div class="hero-title">
        🚀 ReqPilot
    </div>

    <div class="hero-subtitle">
        Transform raw project ideas into structured software requirements,
        Agile user stories, priorities, ambiguity detection and
        development-ready test cases.
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# PROJECT INPUT
# ============================================================

st.markdown("""
<div class="section-label">
    INPUT
</div>

<div class="section-title">
    💡 Describe Your Project
</div>
""", unsafe_allow_html=True)


demo_texts = {

    "College Attendance System":
    """We want to build a college attendance management system where teachers
    can mark attendance and students can view their attendance.
    Students should receive alerts when their attendance is low.""",

    "AI Cold Outreach Platform":
    """We want to build an AI platform that helps sales teams generate
    personalized cold emails from a company profile and target customer
    information. The system should track responses and suggest follow-up messages.""",

    "EV Charging Network":
    """We want to build an EV charging platform where users can find nearby
    charging stations, check availability, reserve a charger and make payments.
    Station owners should be able to manage charging points.""",

    "Student Learning Platform":
    """We want to build an online learning platform for college students.
    Students can watch lessons, complete quizzes and track their progress.
    Teachers can upload courses and monitor student performance.""",

    "Custom Idea":
    ""
}


default_value = demo_texts[preset]


project_idea = st.text_area(
    "Project Idea",
    value=default_value,
    height=170,
    placeholder="Example: Build a college attendance management system...",
    label_visibility="collapsed"
)


# ============================================================
# METRICS
# ============================================================

word_count = len(project_idea.split()) if project_idea.strip() else 0

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{word_count}</div>
        <div class="metric-label">INPUT WORDS</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">6</div>
        <div class="metric-label">AI MODULES</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">6</div>
        <div class="metric-label">OUTPUT ARTIFACTS</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">Gemini</div>
        <div class="metric-label">AI ENGINE</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# PIPELINE
# ============================================================

st.markdown("""
<div class="section-label">
    INTELLIGENCE PIPELINE
</div>

<div class="section-title">
    🔄 From Raw Idea → Engineering Artifacts
</div>
""", unsafe_allow_html=True)


pipeline = [
    ("💡", "Raw Idea", "User Input"),
    ("🧩", "Extract", "Requirements"),
    ("🏷️", "Classify", "Functional / NFR"),
    ("⚡", "Prioritize", "MoSCoW"),
    ("🔎", "Detect Gaps", "Ambiguities"),
    ("🧪", "Test Cases", "Validation")
]


cols = st.columns(6)

for col, item in zip(cols, pipeline):

    icon, title, subtitle = item

    with col:
        st.markdown(f"""
        <div class="pipeline-card">

            <div class="pipeline-icon">
                {icon}
            </div>

            <div class="pipeline-title">
                {title}
            </div>

            <div class="pipeline-subtitle">
                {subtitle}
            </div>

        </div>
        """, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# DEMO DATA
# ============================================================

demo_data = {

    "functional_requirements": [
        "Teachers shall be able to mark attendance for students.",
        "Students shall be able to view their attendance percentage.",
        "The system shall automatically calculate attendance percentage.",
        "The system shall notify students when their attendance falls below the configured threshold."
    ],

    "non_functional_requirements": [
        "The system shall provide secure role-based access for teachers and students.",
        "Attendance records shall be stored reliably.",
        "The system should provide acceptable response time during normal usage."
    ],

    "user_stories": [

        {
            "story": "As a teacher, I want to mark student attendance so that attendance records are maintained digitally.",
            "acceptance_criteria": [
                "Given a teacher is logged in, when they open a class, then they should see the enrolled students.",
                "Given the student list is displayed, when the teacher marks attendance, then the attendance should be saved."
            ]
        },

        {
            "story": "As a student, I want to view my attendance percentage so that I can monitor my attendance.",
            "acceptance_criteria": [
                "Given a student is logged in, when they open attendance, then their current attendance percentage should be displayed.",
                "Given attendance records exist, when the percentage is calculated, then it should reflect the stored attendance data."
            ]
        }
    ],

    "priorities": [
        {
            "requirement": "Teacher attendance marking",
            "priority": "Must Have",
            "reason": "Core functionality of the system."
        },
        {
            "requirement": "Student attendance dashboard",
            "priority": "Must Have",
            "reason": "Required for students to monitor attendance."
        },
        {
            "requirement": "Low attendance alerts",
            "priority": "Should Have",
            "reason": "Important for proactive student notification."
        }
    ],

    "ambiguities": [
        "What attendance percentage should trigger a low-attendance alert?",
        "Should alerts be sent through email, SMS, push notification, or multiple channels?",
        "Should teachers be able to edit attendance after submission?"
    ],

    "test_cases": [

        {
            "id": "TC-001",
            "scenario": "Teacher marks a student present",
            "expected": "Attendance record should be saved successfully."
        },

        {
            "id": "TC-002",
            "scenario": "Student opens attendance dashboard",
            "expected": "Correct attendance percentage should be displayed."
        },

        {
            "id": "TC-003",
            "scenario": "Student attendance falls below threshold",
            "expected": "Low-attendance notification should be triggered."
        }
    ],

    "technical_dependencies": [
        "User authentication",
        "Role-based authorization",
        "Database for attendance records",
        "Notification service",
        "Web-based frontend"
    ]
}


# ============================================================
# GEMINI PROMPT
# ============================================================

def create_prompt(idea):

    return f"""
You are an expert Software Requirements Engineer.

Analyze the following raw project idea and convert it into structured
software engineering artifacts.

PROJECT IDEA:
{idea}

Return ONLY valid JSON.

Use EXACTLY this structure:

{{
    "functional_requirements": [
        "..."
    ],

    "non_functional_requirements": [
        "..."
    ],

    "user_stories": [
        {{
            "story": "...",
            "acceptance_criteria": [
                "Given ..., when ..., then ..."
            ]
        }}
    ],

    "priorities": [
        {{
            "requirement": "...",
            "priority": "Must Have / Should Have / Could Have / Won't Have",
            "reason": "..."
        }}
    ],

    "ambiguities": [
        "..."
    ],

    "test_cases": [
        {{
            "id": "TC-001",
            "scenario": "...",
            "expected": "..."
        }}
    ],

    "technical_dependencies": [
        "..."
    ]
}}

RULES:

1. Extract clear functional requirements.
2. Extract non-functional requirements.
3. Generate useful Agile user stories.
4. Every user story must contain Given/When/Then acceptance criteria.
5. Assign realistic MoSCoW priorities.
6. Identify missing or ambiguous requirements.
7. Generate practical test cases.
8. Identify technical dependencies.
9. Do not invent unnecessary features.
10. Keep the output concise and useful for developers.
"""


# ============================================================
# GEMINI ANALYSIS FUNCTION
# ============================================================

def analyze_with_gemini(idea, api_key):

    if not api_key:
        raise ValueError("Gemini API key is missing.")

    client = genai.Client(api_key=api_key)

    prompt = create_prompt(idea)

    last_error = None

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            text = response.text.strip()

            # Remove accidental markdown fences
            text = re.sub(
                r"^```json\s*",
                "",
                text,
                flags=re.IGNORECASE
            )

            text = re.sub(
                r"^```\s*",
                "",
                text
            )

            text = re.sub(
                r"\s*```$",
                "",
                text
            )

            return json.loads(text)

        except Exception as e:

            last_error = e

            error_text = str(e)

            if "503" in error_text or "UNAVAILABLE" in error_text:

                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue

            raise last_error

    raise last_error


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(data):

    st.markdown("""
    <div class="section-label">
        AI OUTPUT
    </div>

    <div class="section-title">
        ✨ Engineering Analysis
    </div>
    """, unsafe_allow_html=True)


    tabs = st.tabs([
        "📋 Requirements",
        "👤 User Stories",
        "⚡ Priorities",
        "🔎 Gaps",
        "🧪 Test Cases",
        "⚙️ Technical"
    ])


    # --------------------------------------------------------
    # REQUIREMENTS
    # --------------------------------------------------------

    with tabs[0]:

        st.markdown("### Functional Requirements")

        functional = data.get(
            "functional_requirements",
            []
        )

        if functional:

            for i, req in enumerate(functional, 1):
                st.markdown(
                    f"**FR-{i:02d}** — {req}"
                )

        else:
            st.info("No functional requirements generated.")


        st.markdown("### Non-Functional Requirements")

        nonfunctional = data.get(
            "non_functional_requirements",
            []
        )

        if nonfunctional:

            for i, req in enumerate(nonfunctional, 1):
                st.markdown(
                    f"**NFR-{i:02d}** — {req}"
                )

        else:
            st.info("No non-functional requirements generated.")


    # --------------------------------------------------------
    # USER STORIES
    # --------------------------------------------------------

    with tabs[1]:

        stories = data.get(
            "user_stories",
            []
        )

        if not stories:

            st.info("No user stories generated.")

        for i, story in enumerate(stories, 1):

            with st.expander(
                f"User Story {i}",
                expanded=True
            ):

                st.markdown(
                    f"**{story.get('story', '')}**"
                )

                st.markdown("**Acceptance Criteria**")

                criteria = story.get(
                    "acceptance_criteria",
                    []
                )

                for criterion in criteria:

                    st.markdown(
                        f"• {criterion}"
                    )


    # --------------------------------------------------------
    # PRIORITIES
    # --------------------------------------------------------

    with tabs[2]:

        priorities = data.get(
            "priorities",
            []
        )

        if not priorities:

            st.info("No priorities generated.")

        for item in priorities:

            priority = item.get(
                "priority",
                "Unknown"
            )

            st.markdown(f"""
            <div class="glass" style="
                padding:18px;
                margin-bottom:12px;
            ">

                <div style="
                    font-size:16px;
                    font-weight:800;
                    color:white;
                ">
                    {item.get("requirement", "")}
                </div>

                <div style="
                    margin-top:7px;
                    color:#b8c4ff;
                    font-weight:700;
                ">
                    ⚡ {priority}
                </div>

                <div style="
                    margin-top:7px;
                    color:#929db2;
                    font-size:13px;
                ">
                    {item.get("reason", "")}
                </div>

            </div>
            """, unsafe_allow_html=True)


    # --------------------------------------------------------
    # GAPS
    # --------------------------------------------------------

    with tabs[3]:

        ambiguities = data.get(
            "ambiguities",
            []
        )

        if ambiguities:

            st.warning(
                "These points need clarification before development:"
            )

            for i, item in enumerate(
                ambiguities,
                1
            ):

                st.markdown(
                    f"**Q{i}.** {item}"
                )

        else:

            st.success(
                "No major ambiguities detected."
            )


    # --------------------------------------------------------
    # TEST CASES
    # --------------------------------------------------------

    with tabs[4]:

        tests = data.get(
            "test_cases",
            []
        )

        if tests:

            for test in tests:

                st.markdown(f"""
                <div class="glass" style="
                    padding:20px;
                    margin-bottom:14px;
                ">

                    <div style="
                        color:#aebaff;
                        font-size:12px;
                        font-weight:800;
                        letter-spacing:1px;
                    ">
                        {test.get("id", "")}
                    </div>

                    <div style="
                        font-size:17px;
                        font-weight:800;
                        margin-top:6px;
                        color:white;
                    ">
                        {test.get("scenario", "")}
                    </div>

                    <div style="
                        margin-top:10px;
                        color:#9da7ba;
                        font-size:14px;
                    ">
                        <b>Expected:</b>
                        {test.get("expected", "")}
                    </div>

                </div>
                """, unsafe_allow_html=True)

        else:

            st.info("No test cases generated.")


    # --------------------------------------------------------
    # TECHNICAL
    # --------------------------------------------------------

    with tabs[5]:

        dependencies = data.get(
            "technical_dependencies",
            []
        )

        st.markdown("### Technical Dependencies")

        if dependencies:

            for dependency in dependencies:

                st.markdown(
                    f"🔹 {dependency}"
                )

        else:

            st.info(
                "No technical dependencies generated."
            )


    # --------------------------------------------------------
    # JSON DOWNLOAD
    # --------------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    json_data = json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    )

    st.download_button(
        label="⬇️ Download Analysis JSON",
        data=json_data,
        file_name="reqpilot_analysis.json",
        mime="application/json"
    )


# ============================================================
# ACTION BUTTONS
# ============================================================

col1, col2 = st.columns([4, 1])

with col1:

    analyze_button = st.button(
        "⚡ Analyze Requirements",
        type="primary",
        use_container_width=True
    )

with col2:

    demo_button = st.button(
        "🎬 Demo Mode",
        use_container_width=True
    )


# ============================================================
# ANALYZE
# ============================================================

if analyze_button:

    if not project_idea.strip():

        st.warning(
            "Please describe your project idea first."
        )

    elif not api_key:

        st.error(
            "Gemini API key not found. Add GEMINI_API_KEY in Streamlit Secrets."
        )

    else:

        with st.spinner(
            "🧠 ReqPilot is analyzing your requirements..."
        ):

            try:

                result = analyze_with_gemini(
                    project_idea,
                    api_key
                )

                st.success(
                    "✅ Requirements analysis completed!"
                )

                display_results(result)

            except Exception as e:

                error_text = str(e)

                if (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                ):

                    st.error(
                        "⚠️ Gemini is temporarily unavailable. "
                        "Please try again in a moment or use Demo Mode."
                    )

                elif (
                    "429" in error_text
                    or "quota" in error_text.lower()
                ):

                    st.error(
                        "⚠️ API quota/rate limit reached. "
                        "Please try again later or use Demo Mode."
                    )

                else:

                    st.error(
                        f"Execution Error: {error_text}"
                    )


# ============================================================
# DEMO MODE
# ============================================================

if demo_button:

    st.success(
        "🎬 Demo Mode activated — no API call required."
    )

    display_results(demo_data)


# ============================================================
# FEATURES
# ============================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div class="section-label">
    WHY REQPILOT
</div>

<div class="section-title">
    ✨ Built for Requirements Engineering
</div>

<div style="
    color:#9ca6bb;
    margin-bottom:24px;
">
    One raw idea → multiple development-ready artifacts.
</div>
""", unsafe_allow_html=True)


f1, f2, f3 = st.columns(3)


with f1:

    st.markdown("""
    <div class="feature-card">

        <div class="feature-icon">
            📋
        </div>

        <div class="feature-title">
            Requirement Extraction
        </div>

        <div class="feature-text">
            Converts informal project ideas into structured
            functional and non-functional requirements.
        </div>

    </div>
    """, unsafe_allow_html=True)


with f2:

    st.markdown("""
    <div class="feature-card">

        <div class="feature-icon">
            ⚠️
        </div>

        <div class="feature-title">
            Ambiguity Detection
        </div>

        <div class="feature-text">
            Identifies missing, unclear and incomplete
            requirements that need clarification.
        </div>

    </div>
    """, unsafe_allow_html=True)


with f3:

    st.markdown("""
    <div class="feature-card">

        <div class="feature-icon">
            🧪
        </div>

        <div class="feature-title">
            Test Generation
        </div>

        <div class="feature-text">
            Converts requirements into practical test
            scenarios for development and validation.
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# TECHNICAL CONTRIBUTION
# ============================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div class="glass" style="padding:28px;">

    <div style="
        color:#aebaff;
        font-size:12px;
        font-weight:800;
        letter-spacing:2px;
    ">
        TECHNICAL CONTRIBUTION
    </div>

    <div style="
        font-size:23px;
        font-weight:800;
        margin-top:10px;
        color:white;
    ">
        Not just a generic AI wrapper.
    </div>

    <div style="
        color:#9da7ba;
        line-height:1.7;
        margin-top:10px;
    ">
        ReqPilot uses a structured multi-stage requirements analysis
        pipeline covering requirement classification, ambiguity
        detection, prioritization, user-story generation and
        test-case generation from a single project description.
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

    <strong style="color:white;">
        ReqPilot
    </strong>
    • G14 AI Requirements Engineering Agent
    <br><br>

    Built with Python • Streamlit • Generative AI
    <br><br>

    🚀 From raw idea to development-ready requirements

</div>
""", unsafe_allow_html=True)
