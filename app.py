import streamlit as st
import time
import json
from google import genai
from google.genai import types


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FoundersPRD | Requirements Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: #0e1117;
    }

    /* Main container */
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Hero */
    .hero {
        padding: 35px;
        border-radius: 22px;
        background: linear-gradient(
            135deg,
            #151b2b 0%,
            #111827 100%
        );
        border: 1px solid #273449;
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        color: #aab4c5;
        font-size: 18px;
    }

    .badge {
        display: inline-block;
        padding: 6px 13px;
        border-radius: 20px;
        background: #1d4ed8;
        color: white;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 15px;
    }

    /* Section cards */
    .info-card {
        padding: 20px;
        border-radius: 16px;
        background: #151a24;
        border: 1px solid #293241;
        min-height: 120px;
    }

    .info-title {
        font-size: 15px;
        color: #9ca8bb;
        margin-bottom: 8px;
    }

    .info-value {
        font-size: 28px;
        font-weight: 750;
    }

    /* Feature cards */
    .feature-card {
        padding: 22px;
        border-radius: 16px;
        background: #151a24;
        border: 1px solid #293241;
        height: 150px;
    }

    .feature-icon {
        font-size: 28px;
    }

    .feature-title {
        font-weight: 700;
        font-size: 17px;
        margin-top: 8px;
    }

    .feature-text {
        color: #9ca8bb;
        font-size: 14px;
        margin-top: 5px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0b0f16;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 700;
        min-height: 45px;
    }

    /* Text area */
    textarea {
        border-radius: 12px !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        font-weight: 650;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

    <div class="badge">⚡ AI REQUIREMENTS ENGINEERING</div>

    <div class="hero-title">
        🚀 FoundersPRD
    </div>

    <div class="hero-subtitle">
        Transform raw ideas into structured software requirements,
        user stories, priorities and test cases.
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Agent Settings")

    api_key = st.secrets.get("GEMINI_API_KEY", "")

    if not api_key:
        api_key = st.text_input(
            "Enter Gemini API Key:",
            type="password"
        )
    else:
        st.success("✅ API Key Loaded")

    st.markdown("---")

    st.subheader("💡 Demo Ideas")

    preset = st.selectbox(
        "Choose an example:",
        [
            "Custom Idea",
            "College Attendance Management",
            "AI Cold Outreach Tool",
            "Peer-to-Peer EV Charging",
            "Micro-SaaS Churn Predictor"
        ]
    )

    st.markdown("---")

    st.caption("G14 • AI Requirements Engineering Agent")
    st.caption("Built for 24-Hour Hackathon 🚀")


# ============================================================
# PRESET DATA
# ============================================================

sample_pitches = {

    "College Attendance Management":
        """
        We want to build a college attendance management system where
        teachers can mark attendance and students can view their attendance.
        Students should receive alerts when their attendance is low.
        """,

    "AI Cold Outreach Tool":
        """
        We want an AI platform where freelance developers upload their
        portfolio and the system helps create personalized outreach
        messages for potential clients and tracks responses.
        """,

    "Peer-to-Peer EV Charging":
        """
        We want a platform where homeowners with EV chargers can allow
        nearby electric vehicle drivers to book charging slots and make
        payments securely.
        """,

    "Micro-SaaS Churn Predictor":
        """
        We want a lightweight system for online store owners that detects
        customers who may stop using a subscription and provides analytics
        about churn reasons.
        """
}

default_input = sample_pitches.get(preset, "")


# ============================================================
# INPUT SECTION
# ============================================================

st.subheader("💡 Describe Your Project")

startup_pitch = st.text_area(
    "Project Idea / Problem Statement",
    value=default_input,
    height=180,
    placeholder=(
        "Example: We want to build a college attendance system "
        "where teachers mark attendance and students receive alerts..."
    )
)


# ============================================================
# INPUT INFO
# ============================================================

word_count = len(startup_pitch.split())

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-title">📝 Input Words</div>
            <div class="info-value">{word_count}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-title">🤖 AI Engine</div>
            <div class="info-value">Gemini</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-title">🎯 Analysis</div>
            <div class="info-value">6 Modules</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("")


# ============================================================
# GENERATE BUTTON
# ============================================================

generate_btn = st.button(
    "⚡ Generate Requirements",
    type="primary",
    use_container_width=True
)


# ============================================================
# AI GENERATION
# ============================================================

if generate_btn:

    if not api_key:
        st.error("❌ Please provide your Gemini API key.")

    elif not startup_pitch.strip():
        st.warning("⚠️ Please enter a project idea.")

    else:

        client = genai.Client(api_key=api_key)

        # ----------------------------------------------------
        # STRUCTURED PROMPT
        # ----------------------------------------------------

        prompt = f"""
You are an expert AI Requirements Engineering Agent.

Analyze the following software project idea and convert it into
structured software requirements.

PROJECT IDEA:
\"\"\"
{startup_pitch}
\"\"\"

Return ONLY valid JSON.

Use exactly this structure:

{{
    "functional_requirements": [
        "Requirement 1",
        "Requirement 2"
    ],

    "non_functional_requirements": [
        "Requirement 1",
        "Requirement 2"
    ],

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
            "question": "Question that should be asked"
        }}
    ],

    "test_cases": [
        {{
            "id": "TC-01",
            "scenario": "Test scenario",
            "expected_result": "Expected result"
        }}
    ],

    "technical_dependencies": [
        "Database",
        "Authentication",
        "API or service"
    ]
}}

Rules:

1. Do not invent unnecessary features.
2. Identify missing information.
3. Keep requirements clear and testable.
4. Separate functional and non-functional requirements.
5. Prioritize important features.
6. Generate realistic user stories.
7. Generate practical test cases.
8. Return ONLY JSON.
"""


        # ----------------------------------------------------
        # GENERATE WITH RETRY
        # ----------------------------------------------------

        with st.spinner(
            "🤖 AI is analyzing your requirements..."
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

                    if "503" in error_message:

                        if attempt < 2:

                            wait_time = 2 ** attempt

                            st.warning(
                                f"⚠️ Gemini is busy. "
                                f"Retrying in {wait_time} seconds..."
                            )

                            time.sleep(wait_time)

                        else:

                            st.error(
                                "❌ Gemini is temporarily unavailable. "
                                "Please try again."
                            )

                    else:

                        st.error(
                            f"❌ Execution Error: {e}"
                        )

                        break


        # ====================================================
        # PROCESS RESPONSE
        # ====================================================

        if response is not None:

            try:

                data = json.loads(response.text)

                st.success(
                    "✅ Requirements Generated Successfully!"
                )

                st.markdown("---")

                # ------------------------------------------------
                # METRICS
                # ------------------------------------------------

                functional = data.get(
                    "functional_requirements", []
                )

                non_functional = data.get(
                    "non_functional_requirements", []
                )

                stories = data.get(
                    "user_stories", []
                )

                priorities = data.get(
                    "priorities", []
                )

                ambiguities = data.get(
                    "ambiguities", []
                )

                test_cases = data.get(
                    "test_cases", []
                )

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


                st.markdown("")


                # =================================================
                # TABS
                # =================================================

                (
                    tab_req,
                    tab_story,
                    tab_priority,
                    tab_test,
                    tab_risk,
                    tab_tech
                ) = st.tabs(
                    [
                        "📋 Requirements",
                        "👤 User Stories",
                        "🎯 Priority",
                        "🧪 Test Cases",
                        "⚠️ Ambiguities",
                        "🏗️ Technical"
                    ]
                )


                # =================================================
                # REQUIREMENTS
                # =================================================

                with tab_req:

                    st.subheader(
                        "📋 Functional Requirements"
                    )

                    if functional:

                        for i, req in enumerate(
                            functional, 1
                        ):
                            st.markdown(
                                f"**FR-{i:02d}**  {req}"
                            )

                    else:
                        st.info(
                            "No functional requirements detected."
                        )


                    st.markdown("---")

                    st.subheader(
                        "⚙️ Non-Functional Requirements"
                    )

                    if non_functional:

                        for i, req in enumerate(
                            non_functional, 1
                        ):
                            st.markdown(
                                f"**NFR-{i:02d}**  {req}"
                            )

                    else:
                        st.info(
                            "No non-functional requirements detected."
                        )


                # =================================================
                # USER STORIES
                # =================================================

                with tab_story:

                    st.subheader(
                        "👤 Agile User Stories"
                    )

                    for i, story in enumerate(
                        stories, 1
                    ):

                        with st.expander(
                            f"User Story {i}"
                        ):

                            st.markdown(
                                f"**{story.get('story', '')}**"
                            )

                            st.markdown(
                                f"**Priority:** "
                                f"{story.get('priority', 'Not specified')}"
                            )

                            st.markdown(
                                "**Acceptance Criteria**"
                            )

                            criteria = story.get(
                                "acceptance_criteria", []
                            )

                            for criterion in criteria:

                                st.markdown(
                                    f"- {criterion}"
                                )


                # =================================================
                # PRIORITY
                # =================================================

                with tab_priority:

                    st.subheader(
                        "🎯 Feature Prioritization"
                    )

                    for item in priorities:

                        priority = item.get(
                            "priority",
                            "Not specified"
                        )

                        st.markdown(
                            f"""
                            **{item.get('feature', 'Feature')}**

                            Priority: `{priority}`

                            {item.get('reason', '')}
                            """
                        )

                        st.markdown("---")


                # =================================================
                # TEST CASES
                # =================================================

                with tab_test:

                    st.subheader(
                        "🧪 Generated Test Cases"
                    )

                    for test in test_cases:

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

                        st.markdown("---")


                # =================================================
                # AMBIGUITIES
                # =================================================

                with tab_risk:

                    st.subheader(
                        "⚠️ Missing / Ambiguous Requirements"
                    )

                    if ambiguities:

                        for issue in ambiguities:

                            st.warning(
                                f"**Issue:** "
                                f"{issue.get('issue', '')}"
                            )

                            st.info(
                                f"**Question:** "
                                f"{issue.get('question', '')}"
                            )

                    else:

                        st.success(
                            "No major ambiguities detected."
                        )


                # =================================================
                # TECHNICAL DEPENDENCIES
                # =================================================

                with tab_tech:

                    st.subheader(
                        "🏗️ Technical Dependencies"
                    )

                    dependencies = data.get(
                        "technical_dependencies", []
                    )

                    for dependency in dependencies:

                        st.markdown(
                            f"🔹 {dependency}"
                        )


                # =================================================
                # DOWNLOAD JSON
                # =================================================

                st.markdown("---")

                st.subheader(
                    "📥 Export Requirements"
                )

                download_data = json.dumps(
                    data,
                    indent=4,
                    ensure_ascii=False
                )

                st.download_button(
                    label="📥 Download Requirements (JSON)",
                    data=download_data,
                    file_name="requirements.json",
                    mime="application/json",
                    use_container_width=True
                )


            except Exception as e:

                st.error(
                    "⚠️ AI returned an unexpected format."
                )

                st.code(
                    response.text,
                    language="text"
                )

                st.caption(
                    f"Parsing error: {e}"
                )


# ============================================================
# FEATURES SECTION
# ============================================================

if not generate_btn:

    st.markdown("---")

    st.subheader("✨ What FoundersPRD Does")

    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📋</div>
            <div class="feature-title">
                Requirement Extraction
            </div>
            <div class="feature-text">
                Converts raw project ideas into structured
                functional and non-functional requirements.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">👤</div>
            <div class="feature-title">
                Agile User Stories
            </div>
            <div class="feature-text">
                Generates user stories with acceptance
                criteria for development teams.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧪</div>
            <div class="feature-title">
                Test Case Generation
            </div>
            <div class="feature-text">
                Creates practical test scenarios directly
                from the identified requirements.
            </div>
        </div>
        """, unsafe_allow_html=True)
