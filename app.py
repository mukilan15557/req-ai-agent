import streamlit as st
import json
import time

from google import genai
from google.genai import types


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ReqPilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CSS - LIQUID GLASS LOOK
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(100, 80, 255, 0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(0, 170, 255, 0.15),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(170, 70, 255, 0.12),
                transparent 35%
            ),
            #080b12;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Glass containers */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.055);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 22px;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.07);
    }

    /* Text */
    h1, h2, h3 {
        color: white !important;
    }

    p, li {
        color: #c1c8d8;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 15px;
        min-height: 48px;
        font-weight: 700;
        border: 1px solid rgba(255,255,255,0.15);
        background: rgba(255,255,255,0.07);
        color: white;
        transition: 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        border-color: rgba(150,160,255,0.5);
    }

    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(
            135deg,
            #7165ff,
            #9879ff
        );
        color: white;
        border: none;
        box-shadow: 0 10px 35px rgba(110, 90, 255, 0.35);
    }

    /* Text area */
    textarea {
        background: rgba(255,255,255,0.055) !important;
        color: white !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.13) !important;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        color: #aeb7c9 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: white !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(8, 11, 18, 0.96);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* Hide Streamlit footer */
    footer {
        visibility: hidden;
    }

    #MainMenu {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🚀 ReqPilot")

    st.caption("AI Requirements Engineering Agent")

    st.divider()

    st.subheader("🔐 AI Connection")

    api_key = None

    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            st.success("✓ Gemini API Connected")
        else:
            api_key = st.text_input(
                "Gemini API Key",
                type="password"
            )
    except Exception:
        api_key = st.text_input(
            "Gemini API Key",
            type="password"
        )

    st.divider()

    st.subheader("🎯 Demo Presets")

    preset = st.selectbox(
        "Choose project",
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

    st.write("01  →  Requirement Extraction")
    st.write("02  →  Requirement Classification")
    st.write("03  →  Priority Analysis")
    st.write("04  →  Ambiguity Detection")
    st.write("05  →  User Story Generation")
    st.write("06  →  Test Case Generation")

    st.divider()

    st.caption("G14 • Hackathon Prototype")


# =========================================================
# HERO
# =========================================================

with st.container(border=True):

    st.caption("G14 • AI REQUIREMENTS ENGINEERING AGENT")

    st.title("🚀 ReqPilot")

    st.write(
        "Transform raw project ideas into structured software "
        "requirements, Agile user stories, priorities, "
        "ambiguity detection and development-ready test cases."
    )


# =========================================================
# DEMO INPUT DATA
# =========================================================

demo_texts = {

    "Custom Idea": "",

    "College Attendance System":
        """We want to build a college attendance management system
        where teachers can mark attendance and students can view
        their attendance. Students should receive alerts when their
        attendance is low.""",

    "AI Cold Outreach Platform":
        """We want to build an AI platform that helps sales teams
        generate personalized cold emails from company profiles
        and target customer information. The system should track
        responses and suggest follow-up messages.""",

    "EV Charging Network":
        """We want to build an EV charging platform where users can
        find nearby charging stations, check availability, reserve
        a charger and make payments. Station owners should manage
        charging points.""",

    "Student Learning Platform":
        """We want to build an online learning platform for college
        students. Students can watch lessons, complete quizzes and
        track progress. Teachers can upload courses and monitor
        student performance."""
}


# =========================================================
# INPUT
# =========================================================

st.subheader("💡 Describe Your Project")

project_idea = st.text_area(
    "Project idea",
    value=demo_texts[preset],
    height=170,
    placeholder=(
        "Example: Build a college attendance management "
        "system for teachers and students..."
    ),
    label_visibility="collapsed"
)


# =========================================================
# METRICS
# =========================================================

word_count = len(project_idea.split()) if project_idea.strip() else 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    with st.container(border=True):
        st.metric("Input Words", word_count)

with c2:
    with st.container(border=True):
        st.metric("AI Modules", 6)

with c3:
    with st.container(border=True):
        st.metric("Artifacts", 6)

with c4:
    with st.container(border=True):
        st.metric("AI Engine", "Gemini")


# =========================================================
# PIPELINE
# =========================================================

st.subheader("🔄 Intelligence Pipeline")

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
        with st.container(border=True):
            st.markdown(f"### {icon}")
            st.write(f"**{title}**")
            st.caption(subtitle)


# =========================================================
# DEMO DATA
# =========================================================

demo_data = {

    "functional_requirements": [
        "Teachers shall be able to mark attendance for students.",
        "Students shall be able to view their attendance percentage.",
        "The system shall automatically calculate attendance percentage.",
        "The system shall notify students when attendance falls below the configured threshold."
    ],

    "non_functional_requirements": [
        "The system shall provide secure role-based access.",
        "Attendance records shall be stored reliably.",
        "The system should provide acceptable response time."
    ],

    "user_stories": [

        {
            "story":
                "As a teacher, I want to mark student attendance "
                "so that attendance records are maintained digitally.",

            "acceptance_criteria": [
                "Given a teacher is logged in, when they open a class, then enrolled students should be displayed.",
                "Given the student list is displayed, when attendance is marked, then the record should be saved."
            ]
        },

        {
            "story":
                "As a student, I want to view my attendance percentage "
                "so that I can monitor my attendance.",

            "acceptance_criteria": [
                "Given a student is logged in, when they open attendance, then their percentage should be displayed.",
                "Given attendance records exist, when the percentage is calculated, then it should reflect stored data."
            ]
        }
    ],

    "priorities": [

        {
            "requirement": "Teacher attendance marking",
            "priority": "Must Have",
            "reason": "Core functionality."
        },

        {
            "requirement": "Student attendance dashboard",
            "priority": "Must Have",
            "reason": "Required for attendance monitoring."
        },

        {
            "requirement": "Low attendance alerts",
            "priority": "Should Have",
            "reason": "Useful for proactive notification."
        }
    ],

    "ambiguities": [
        "What attendance percentage should trigger an alert?",
        "Should alerts use email, SMS, push notification, or multiple channels?",
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
            "scenario": "Attendance falls below threshold",
            "expected": "Low-attendance notification should be triggered."
        }
    ],

    "technical_dependencies": [
        "User authentication",
        "Role-based authorization",
        "Attendance database",
        "Notification service",
        "Web frontend"
    ]
}


# =========================================================
# GEMINI PROMPT
# =========================================================

def create_prompt(idea):

    return f"""
You are an expert Software Requirements Engineer.

Analyze this project idea:

{idea}

Return ONLY valid JSON.

Use exactly this structure:

{{
  "functional_requirements": [],
  "non_functional_requirements": [],
  "user_stories": [
    {{
      "story": "",
      "acceptance_criteria": []
    }}
  ],
  "priorities": [
    {{
      "requirement": "",
      "priority": "",
      "reason": ""
    }}
  ],
  "ambiguities": [],
  "test_cases": [
    {{
      "id": "",
      "scenario": "",
      "expected": ""
    }}
  ],
  "technical_dependencies": []
}}

Rules:

1. Extract functional requirements.
2. Extract non-functional requirements.
3. Generate useful Agile user stories.
4. Use Given / When / Then acceptance criteria.
5. Assign MoSCoW priorities.
6. Identify unclear or missing requirements.
7. Generate practical test cases.
8. Identify technical dependencies.
9. Do not invent unnecessary features.
10. Keep the result concise and useful for developers.
"""


# =========================================================
# GEMINI FUNCTION
# =========================================================

def analyze_with_gemini(idea, key):

    client = genai.Client(api_key=key)

    prompt = create_prompt(idea)

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            return json.loads(response.text)

        except Exception as e:

            error_text = str(e)

            if (
                ("503" in error_text or "UNAVAILABLE" in error_text)
                and attempt < 2
            ):
                time.sleep(2 ** attempt)
                continue

            raise e


# =========================================================
# RESULT DISPLAY
# =========================================================

def display_results(data):

    st.subheader("✨ Engineering Analysis")

    tabs = st.tabs(
        [
            "📋 Requirements",
            "👤 User Stories",
            "⚡ Priorities",
            "🔎 Gaps",
            "🧪 Test Cases",
            "⚙️ Technical"
        ]
    )


    # -----------------------------------------------------
    # REQUIREMENTS
    # -----------------------------------------------------

    with tabs[0]:

        st.markdown("### Functional Requirements")

        requirements = data.get(
            "functional_requirements",
            []
        )

        for i, req in enumerate(requirements, 1):

            with st.container(border=True):
                st.write(f"**FR-{i:02d}**")
                st.write(req)


        st.markdown("### Non-Functional Requirements")

        nfr = data.get(
            "non_functional_requirements",
            []
        )

        for i, req in enumerate(nfr, 1):

            with st.container(border=True):
                st.write(f"**NFR-{i:02d}**")
                st.write(req)


    # -----------------------------------------------------
    # USER STORIES
    # -----------------------------------------------------

    with tabs[1]:

        stories = data.get(
            "user_stories",
            []
        )

        for i, story in enumerate(stories, 1):

            with st.container(border=True):

                st.markdown(f"### User Story {i}")

                st.write(
                    story.get("story", "")
                )

                st.markdown(
                    "**Acceptance Criteria**"
                )

                for criterion in story.get(
                    "acceptance_criteria",
                    []
                ):

                    st.write(
                        f"• {criterion}"
                    )


    # -----------------------------------------------------
    # PRIORITIES
    # -----------------------------------------------------

    with tabs[2]:

        priorities = data.get(
            "priorities",
            []
        )

        for item in priorities:

            with st.container(border=True):

                st.markdown(
                    f"### {item.get('requirement', '')}"
                )

                st.write(
                    f"⚡ **{item.get('priority', '')}**"
                )

                st.caption(
                    item.get("reason", "")
                )


    # -----------------------------------------------------
    # GAPS
    # -----------------------------------------------------

    with tabs[3]:

        ambiguities = data.get(
            "ambiguities",
            []
        )

        if ambiguities:

            st.warning(
                "These requirements need clarification:"
            )

            for i, question in enumerate(
                ambiguities,
                1
            ):

                with st.container(border=True):
                    st.write(
                        f"**Q{i}.** {question}"
                    )

        else:

            st.success(
                "No major ambiguities detected."
            )


    # -----------------------------------------------------
    # TEST CASES
    # -----------------------------------------------------

    with tabs[4]:

        tests = data.get(
            "test_cases",
            []
        )

        for test in tests:

            with st.container(border=True):

                st.caption(
                    test.get("id", "")
                )

                st.markdown(
                    f"### {test.get('scenario', '')}"
                )

                st.write(
                    f"**Expected:** {test.get('expected', '')}"
                )


    # -----------------------------------------------------
    # TECHNICAL
    # -----------------------------------------------------

    with tabs[5]:

        st.markdown(
            "### Technical Dependencies"
        )

        dependencies = data.get(
            "technical_dependencies",
            []
        )

        for dependency in dependencies:

            st.write(
                f"🔹 {dependency}"
            )


    # -----------------------------------------------------
    # DOWNLOAD
    # -----------------------------------------------------

    st.divider()

    json_output = json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    )

    st.download_button(
        "⬇️ Download Analysis JSON",
        json_output,
        "reqpilot_analysis.json",
        "application/json"
    )


# =========================================================
# BUTTONS
# =========================================================

button1, button2 = st.columns([4, 1])

with button1:

    analyze = st.button(
        "⚡ Analyze Requirements",
        type="primary",
        use_container_width=True
    )

with button2:

    demo = st.button(
        "🎬 Demo Mode",
        use_container_width=True
    )


# =========================================================
# ANALYZE
# =========================================================

if analyze:

    if not project_idea.strip():

        st.warning(
            "💡 Please enter a project idea first."
        )

    elif not api_key:

        st.error(
            "🔐 Gemini API key not found."
        )

    else:

        with st.spinner(
            "🧠 ReqPilot is analyzing your project..."
        ):

            try:

                result = analyze_with_gemini(
                    project_idea,
                    api_key
                )

                st.success(
                    "✅ Analysis completed successfully!"
                )

                display_results(result)

            except Exception as e:

                error = str(e)

                if (
                    "503" in error
                    or "UNAVAILABLE" in error
                ):

                    st.error(
                        "⚠️ Gemini is temporarily busy. "
                        "Please try again or use Demo Mode."
                    )

                elif (
                    "429" in error
                    or "quota" in error.lower()
                ):

                    st.error(
                        "⚠️ API quota/rate limit reached. "
                        "Try Demo Mode."
                    )

                else:

                    st.error(
                        f"❌ Error: {error}"
                    )


# =========================================================
# DEMO MODE
# =========================================================

if demo:

    st.success(
        "🎬 Demo Mode — No API call required."
    )

    display_results(demo_data)


# =========================================================
# FEATURES
# =========================================================

st.divider()

st.subheader("✨ Built for Requirements Engineering")

f1, f2, f3 = st.columns(3)

with f1:

    with st.container(border=True):

        st.markdown("### 📋 Requirement Extraction")

        st.write(
            "Converts informal project ideas into "
            "structured functional and non-functional requirements."
        )


with f2:

    with st.container(border=True):

        st.markdown("### ⚠️ Ambiguity Detection")

        st.write(
            "Identifies missing, unclear and incomplete "
            "requirements that need clarification."
        )


with f3:

    with st.container(border=True):

        st.markdown("### 🧪 Test Generation")

        st.write(
            "Converts requirements into practical "
            "test scenarios for development and validation."
        )


# =========================================================
# TECHNICAL CONTRIBUTION
# =========================================================

st.divider()

with st.container(border=True):

    st.subheader(
        "🧠 Technical Contribution"
    )

    st.write(
        "Our solution is not just a generic API wrapper. "
        "ReqPilot uses a structured multi-stage requirements "
        "analysis pipeline covering requirement classification, "
        "ambiguity detection, prioritization, user-story generation "
        "and test-case generation from a single project description."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🚀 ReqPilot • G14 AI Requirements Engineering Agent • "
    "Python • Streamlit • Generative AI"
)
