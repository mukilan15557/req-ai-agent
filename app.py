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
# APP HEADER
# ============================================================

st.title("🚀 ReqPilot")

st.subheader("AI Requirements Engineering Agent")

st.write(
    "Transform raw project ideas into structured software requirements, "
    "user stories, priorities, ambiguity analysis and test cases."
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Agent Control")

    api_key = st.secrets.get("GEMINI_API_KEY", "")

    if api_key:
        st.success("✅ Gemini API Connected")
    else:
        api_key = st.text_input(
            "Enter Gemini API Key",
            type="password"
        )

    st.divider()

    st.subheader("💡 Demo Presets")

    preset = st.selectbox(
        "Choose a project idea",
        [
            "Custom Idea",
            "College Attendance System",
            "AI Cold Outreach Platform",
            "EV Charging Network",
            "Student Learning Platform"
        ]
    )

    st.divider()

    st.subheader("🧠 Analysis Pipeline")

    st.write("1️⃣ Requirement Extraction")
    st.write("2️⃣ Requirement Classification")
    st.write("3️⃣ Feature Prioritization")
    st.write("4️⃣ Ambiguity Detection")
    st.write("5️⃣ User Story Generation")
    st.write("6️⃣ Test Case Generation")

    st.divider()

    st.caption("G14 • AI Requirements Engineering Agent")
    st.caption("24-Hour Hackathon Project 🚀")


# ============================================================
# PRESET PROJECTS
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
# PROJECT INPUT
# ============================================================

st.header("💡 Describe Your Project")

st.write(
    "Enter a raw idea, problem statement or incomplete project notes."
)

startup_pitch = st.text_area(
    "Project Idea",
    value=default_input,
    height=180,
    placeholder=(
        "Example: We want to build a college attendance system "
        "where teachers mark attendance and students receive alerts..."
    )
)


# ============================================================
# INPUT INFORMATION
# ============================================================

word_count = len(startup_pitch.split())

col1, col2, col3 = st.columns(3)

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
        "🎯 Output Type",
        "Structured"
    )


# ============================================================
# PIPELINE
# ============================================================

st.subheader("🔄 AI Analysis Pipeline")

pipeline_cols = st.columns(6)

pipeline_steps = [
    ("💡", "Raw Idea"),
    ("🔍", "Extract"),
    ("🎯", "Prioritize"),
    ("⚠️", "Detect Gaps"),
    ("👤", "User Stories"),
    ("🧪", "Test Cases")
]

for col, (icon, label) in zip(
    pipeline_cols,
    pipeline_steps
):

    with col:
        st.info(f"{icon}\n\n**{label}**")


# ============================================================
# BUTTONS
# ============================================================

st.divider()

generate_col, demo_col = st.columns([3, 1])

with generate_col:

    generate_btn = st.button(
        "⚡ Analyze Requirements",
        type="primary",
        use_container_width=True
    )

with demo_col:

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

                "Given a teacher is logged in, when attendance is submitted, "
                "then the attendance record should be saved.",

                "Given attendance submission fails, when the teacher retries, "
                "then the system should display an appropriate error."
            ]
        },

        {
            "story":
                "As a student, I want to view my attendance percentage "
                "so that I can monitor my attendance status.",

            "priority":
                "Must Have",

            "acceptance_criteria": [

                "Given attendance records exist, when the student opens "
                "the dashboard, then the current percentage should be displayed.",

                "Given attendance data is unavailable, when the dashboard "
                "loads, then the system should display an appropriate message."
            ]
        }
    ],

    "priorities": [

        {
            "feature":
                "Teacher Attendance Entry",

            "priority":
                "Must Have",

            "reason":
                "Core functionality of the attendance system."
        },

        {
            "feature":
                "Student Attendance Dashboard",

            "priority":
                "Must Have",

            "reason":
                "Students need to monitor their attendance."
        },

        {
            "feature":
                "Low Attendance Alerts",

            "priority":
                "Should Have",

            "reason":
                "Provides proactive notification to students."
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
            "id":
                "TC-01",

            "scenario":
                "Teacher submits attendance successfully.",

            "expected_result":
                "Attendance records are saved and reflected in student dashboards."
        },

        {
            "id":
                "TC-02",

            "scenario":
                "Student attendance falls below the threshold.",

            "expected_result":
                "The student receives a low-attendance notification."
        },

        {
            "id":
                "TC-03",

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
# RESULT DISPLAY FUNCTION
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
    # RESULT HEADER
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
            "⚠️ Ambiguities",
            len(ambiguities)
        )


    # ========================================================
    # RESULT TABS
    # ========================================================

    tabs = st.tabs(
        [
            "📋 Requirements",
            "👤 User Stories",
            "🎯 Priorities",
            "🧪 Test Cases",
            "⚠️ Gaps & Risks",
            "🏗️ Technical"
        ]
    )


    # ========================================================
    # REQUIREMENTS TAB
    # ========================================================

    with tabs[0]:

        st.subheader("📋 Functional Requirements")

        if functional:

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

        else:

            st.info(
                "No functional requirements detected."
            )


        st.subheader(
            "⚙️ Non-Functional Requirements"
        )

        if non_functional:

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

        else:

            st.info(
                "No non-functional requirements detected."
            )


    # ========================================================
    # USER STORIES TAB
    # ========================================================

    with tabs[1]:

        st.subheader(
            "👤 Agile User Stories"
        )

        if stories:

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

                    criteria = story.get(
                        "acceptance_criteria",
                        []
                    )

                    for criterion in criteria:

                        st.write(
                            f"✓ {criterion}"
                        )

        else:

            st.info(
                "No user stories generated."
            )


    # ========================================================
    # PRIORITY TAB
    # ========================================================

    with tabs[2]:

        st.subheader(
            "🎯 Feature Prioritization"
        )

        if priorities:

            for item in priorities:

                with st.container(border=True):

                    st.markdown(
                        f"### {item.get('feature', 'Feature')}"
                    )

                    st.write(
                        f"**Priority:** "
                        f"{item.get('priority', 'Not specified')}"
                    )

                    st.write(
                        item.get(
                            "reason",
                            ""
                        )
                    )

        else:

            st.info(
                "No priorities generated."
            )


    # ========================================================
    # TEST CASE TAB
    # ========================================================

    with tabs[3]:

        st.subheader(
            "🧪 Generated Test Cases"
        )

        if test_cases:

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

        else:

            st.info(
                "No test cases generated."
            )


    # ========================================================
    # GAPS TAB
    # ========================================================

    with tabs[4]:

        st.subheader(
            "⚠️ Missing & Ambiguous Requirements"
        )

        if ambiguities:

            for issue in ambiguities:

                st.warning(
                    f"**Gap:** "
                    f"{issue.get('issue', '')}"
                )

                st.info(
                    f"💬 **Clarification:** "
                    f"{issue.get('question', '')}"
                )

        else:

            st.success(
                "✅ No major ambiguities detected."
            )


    # ========================================================
    # TECHNICAL TAB
    # ========================================================

    with tabs[5]:

        st.subheader(
            "🏗️ Technical Dependencies"
        )

        if dependencies:

            for dependency in dependencies:

                st.write(
                    f"🔹 {dependency}"
                )

        else:

            st.info(
                "No technical dependencies detected."
            )


    # ========================================================
    # DOWNLOAD
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
        label="📥 Download Requirements JSON",
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
        "🎬 Demo Mode activated — no Gemini API request used."
    )

    display_results(
        demo_data
    )


# ============================================================
# REAL GEMINI GENERATION
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


        # ====================================================
        # AI PROMPT
        # ====================================================

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

Rules:

1. Extract functional requirements.
2. Extract non-functional requirements.
3. Generate realistic Agile user stories.
4. Include Given / When / Then acceptance criteria.
5. Prioritize important features.
6. Detect missing and ambiguous requirements.
7. Generate practical test cases.
8. Identify technical dependencies.
9. Do not invent unnecessary features.
10. Keep requirements clear and testable.
11. Return ONLY valid JSON.
"""


        # ====================================================
        # API REQUEST
        # ====================================================

        with st.spinner(
            "🤖 ReqPilot is analyzing your project..."
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


                    # ----------------------------------------
                    # 503 TEMPORARY ERROR
                    # ----------------------------------------

                    if "503" in error_message:

                        if attempt < 2:

                            wait_time = 2 ** attempt

                            st.warning(
                                f"⚠️ Gemini is temporarily busy. "
                                f"Retrying in {wait_time} seconds..."
                            )

                            time.sleep(
                                wait_time
                            )

                        else:

                            st.error(
                                "❌ Gemini is temporarily unavailable."
                            )

                            st.info(
                                "Please try again after a short wait."
                            )


                    # ----------------------------------------
                    # 429 QUOTA ERROR
                    # ----------------------------------------

                    elif "429" in error_message:

                        st.error(
                            "🚫 Gemini API quota has been reached."
                        )

                        st.info(
                            "Use 🎬 Demo Mode to demonstrate "
                            "the complete frontend without another API request."
                        )

                        break


                    # ----------------------------------------
                    # OTHER ERROR
                    # ----------------------------------------

                    else:

                        st.error(
                            f"❌ Execution Error: {e}"
                        )

                        break


        # ====================================================
        # PROCESS AI RESPONSE
        # ====================================================

        if response is not None:

            try:

                data = json.loads(
                    response.text
                )

                st.success(
                    "✅ Requirements Generated Successfully!"
                )

                display_results(
                    data
                )

            except Exception as e:

                st.error(
                    "⚠️ AI returned an unexpected format."
                )

                st.code(
                    response.text,
                    language="json"
                )

                st.caption(
                    f"Parsing error: {e}"
                )


# ============================================================
# LANDING PAGE
# ============================================================

if not generate_btn and not demo_btn:

    st.divider()

    st.header(
        "✨ What ReqPilot Can Do"
    )

    st.write(
        "From one raw idea to multiple development-ready artifacts."
    )

    f1, f2, f3 = st.columns(3)

    with f1:

        with st.container(border=True):

            st.subheader(
                "📋 Requirement Extraction"
            )

            st.write(
                "Converts informal project ideas into "
                "functional and non-functional requirements."
            )


    with f2:

        with st.container(border=True):

            st.subheader(
                "⚠️ Ambiguity Detection"
            )

            st.write(
                "Identifies missing information and "
                "generates clarification questions."
            )


    with f3:

        with st.container(border=True):

            st.subheader(
                "🧪 Test Generation"
            )

            st.write(
                "Creates practical test cases directly "
                "from identified requirements."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ReqPilot • G14 AI Requirements Engineering Agent • "
    "Built with Python + Streamlit + Generative AI"
)
