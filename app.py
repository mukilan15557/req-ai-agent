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
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# =========================================================
# GLASSMORPHISM UI
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(90, 70, 180, 0.22), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(0, 170, 255, 0.16), transparent 28%),
        radial-gradient(circle at 50% 100%, rgba(150, 50, 200, 0.14), transparent 35%),
        #080b14;
    color: #f5f7ff;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.055);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 22px;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    box-shadow:
        0 8px 32px rgba(0, 0, 0, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.06);
    padding: 8px;
}

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

p {
    color: rgba(240, 243, 255, 0.78);
}

.stButton > button {
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.14);
    background: rgba(255,255,255,0.07);
    color: white;
    font-weight: 650;
    min-height: 45px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: rgba(255,255,255,0.13);
    border-color: rgba(255,255,255,0.25);
    transform: translateY(-1px);
}

.stButton > button[kind="primary"] {
    background: linear-gradient(
        135deg,
        rgba(116, 80, 255, 0.85),
        rgba(0, 174, 255, 0.75)
    );
    border: 1px solid rgba(255,255,255,0.18);
}

textarea {
    background: rgba(255,255,255,0.055) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 16px !important;
    color: white !important;
}

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.06);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.12);
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.09);
    padding: 14px;
    border-radius: 16px;
}

button[data-baseweb="tab"] {
    color: rgba(255,255,255,0.7);
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: white;
}

section[data-testid="stSidebar"] {
    background: rgba(7, 9, 18, 0.82);
    border-right: 1px solid rgba(255,255,255,0.08);
}

hr {
    border-color: rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOGIN
# =========================================================

if not st.session_state.logged_in:

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:

        with st.container(border=True):

            st.markdown(
                "<h1 style='text-align:center;'>🚀 ReqPilot</h1>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<p style='text-align:center;'>"
                "AI Requirements Engineering Agent"
                "</p>",
                unsafe_allow_html=True
            )

            st.divider()

            username = st.text_input(
                "👤 Username",
                placeholder="Enter username"
            )

            password = st.text_input(
                "🔒 Password",
                type="password",
                placeholder="Enter password"
            )

            st.write("")

            if st.button(
                "🚀 Login",
                type="primary",
                use_container_width=True
            ):

                if username == "reqpilot" and password == "reqpilot123":

                    st.session_state.logged_in = True

                    st.success(
                        "Login successful! 🎉"
                    )

                    time.sleep(0.5)

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid username or password."
                    )

            st.write("")

            st.caption(
                "Demo Login: reqpilot / reqpilot123"
            )

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🚀 ReqPilot")

    st.caption(
        "AI Requirements Engineering Agent"
    )

    st.divider()

    # API KEY

    st.subheader("🔑 AI Connection")

    api_key = None

    try:

        api_key = st.secrets["GEMINI_API_KEY"]

        st.success(
            "API Key Loaded from Secrets"
        )

    except Exception:

        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="Enter API key"
        )

    st.divider()

    # PRESET

    st.subheader("🎬 Demo Preset")

    preset = st.selectbox(
        "Choose a product idea",
        [
            "Custom Idea",
            "QuickCart Grocery Platform",
            "AI Fitness Platform",
            "EV Charging Platform",
            "Student Learning Platform"
        ]
    )

    st.divider()

    # PIPELINE

    st.subheader("⚙️ Pipeline")

    st.write("💡 Raw Idea")
    st.write("🧩 Requirement Extraction")
    st.write("🏷️ Classification")
    st.write("⚡ Prioritization")
    st.write("🔎 Gap Detection")
    st.write("🧪 Test Generation")

    st.divider()

    st.caption(
        "G14 • AI Requirements Engineering Agent"
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.rerun()


# =========================================================
# DEMO INPUTS
# =========================================================

demo_inputs = {

    "QuickCart Grocery Platform": """
We want to build QuickCart, a grocery delivery platform.

Users should be able to create accounts, browse and search for groceries,
add products to a cart, make online payments, place orders, track deliveries,
and receive order notifications.

The platform should securely handle user information and payments, support
multiple users, and provide a reliable shopping experience.
""",

    "AI Fitness Platform": """
We want to build an AI fitness platform where users can create profiles,
set fitness goals, follow personalized workout plans, track progress,
and receive recommendations based on their activity.
""",

    "EV Charging Platform": """
We want to build an EV charging platform where electric vehicle owners
can find nearby charging stations, check availability, reserve a charging
slot, make payments, and receive notifications when charging is complete.
""",

    "Student Learning Platform": """
We want to build a student learning platform where students can access
courses, watch lessons, complete quizzes, track their progress, and receive
personalized learning recommendations.
"""
}


# =========================================================
# HERO
# =========================================================

with st.container(border=True):

    st.caption(
        "G14 • AI REQUIREMENTS ENGINEERING AGENT"
    )

    st.title("🚀 ReqPilot")

    st.write(
        "Turn an informal product idea into structured, "
        "development-ready software requirements using AI."
    )

    st.write(
        "Requirements • User Stories • Priorities • "
        "Gaps • Test Cases • Dependencies"
    )


# =========================================================
# INPUT
# =========================================================

st.write("")

if preset == "Custom Idea":

    default_text = ""

else:

    default_text = demo_inputs[preset]


with st.container(border=True):

    st.subheader("💡 Describe Your Product")

    idea = st.text_area(
        "Product / Startup Idea",
        value=default_text,
        height=190,
        placeholder=(
            "Example: We want to build an online grocery "
            "delivery platform where users can..."
        ),
        label_visibility="collapsed"
    )


# =========================================================
# METRICS
# =========================================================

word_count = len(idea.split()) if idea.strip() else 0

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Input Words", word_count)

with m2:
    st.metric("AI Modules", "6")

with m3:
    st.metric("Artifacts", "6")

with m4:
    st.metric("AI Engine", "Gemini")


# =========================================================
# PIPELINE
# =========================================================

st.write("")

st.subheader(
    "🔄 Requirement Intelligence Pipeline"
)

pipeline = [

    ("💡", "Raw Idea", "User Input"),
    ("🧩", "Extract", "Requirements"),
    ("🏷️", "Classify", "FR / NFR"),
    ("⚡", "Prioritize", "MoSCoW"),
    ("🔎", "Detect Gaps", "Ambiguities"),
    ("🧪", "Test Cases", "Validation")
]

cols = st.columns(6)

for col, item in zip(cols, pipeline):

    icon, title, subtitle = item

    with col:

        with st.container(border=True):

            st.markdown(
                f"### {icon}"
            )

            st.write(
                f"**{title}**"
            )

            st.caption(
                subtitle
            )


# =========================================================
# PROPER QUICKCART DEMO DATA
# =========================================================

demo_data = {

    "functional_requirements": [

        "Users should be able to register and securely log in.",

        "Users should be able to browse groceries by category.",

        "Users should be able to search for grocery products.",

        "Users should be able to add products to a shopping cart and update quantities.",

        "Users should be able to place grocery orders and make online payments.",

        "Users should be able to track the delivery status of their orders."
    ],

    "non_functional_requirements": [

        "User personal and payment information must be securely protected.",

        "The application should provide fast response times during normal usage.",

        "The platform should remain available during high-demand periods.",

        "The system should support multiple users simultaneously."
    ],

    "user_stories": [

        {
            "story":
                "As a customer, I want to create an account and log in so that I can securely manage my grocery orders.",

            "acceptance_criteria": [

                "Given a new user provides valid details, when registration is submitted, then an account should be created.",

                "Given a registered user enters valid credentials, when they log in, then they should access their account."
            ]
        },

        {
            "story":
                "As a customer, I want to search and browse groceries so that I can quickly find products I need.",

            "acceptance_criteria": [

                "Given products exist, when the user searches by product name, then matching products should be displayed.",

                "Given products belong to categories, when the user selects a category, then relevant products should be displayed."
            ]
        },

        {
            "story":
                "As a customer, I want to add products to my cart and update quantities so that I can prepare my order.",

            "acceptance_criteria": [

                "Given a product is available, when the user selects Add to Cart, then the product should appear in the cart.",

                "When the user changes quantity, then the cart total should update correctly."
            ]
        },

        {
            "story":
                "As a customer, I want to place an order and pay online so that my groceries can be delivered.",

            "acceptance_criteria": [

                "Given the cart contains products, when payment succeeds, then the order should be created.",

                "Given payment fails, when checkout is attempted, then the order should not be confirmed."
            ]
        },

        {
            "story":
                "As a customer, I want to track my delivery so that I know the current status of my order.",

            "acceptance_criteria": [

                "Given an order exists, when the user opens order tracking, then the current status should be displayed.",

                "When delivery status changes, the user should receive an update."
            ]
        }
    ],

    "priorities": [

        {
            "requirement":
                "User registration and login",
            "priority":
                "Must Have",
            "reason":
                "Required for secure account and order management."
        },

        {
            "requirement":
                "Product browsing and search",
            "priority":
                "Must Have",
            "reason":
                "Core functionality for discovering groceries."
        },

        {
            "requirement":
                "Shopping cart",
            "priority":
                "Must Have",
            "reason":
                "Required before checkout and order placement."
        },

        {
            "requirement":
                "Online payment",
            "priority":
                "Must Have",
            "reason":
                "Required to complete online purchases."
        },

        {
            "requirement":
                "Order tracking",
            "priority":
                "Should Have",
            "reason":
                "Provides visibility into delivery progress."
        },

        {
            "requirement":
                "Personalized recommendations",
            "priority":
                "Could Have",
            "reason":
                "Useful enhancement but not required for the core platform."
        }
    ],

    "ambiguities": [

        "Which payment methods should be supported?",

        "Which geographical areas should the delivery service cover?",

        "What should happen if a product becomes unavailable after being added to the cart?",

        "Can customers cancel an order after payment?",

        "What is the expected delivery time?",

        "Should notifications use email, SMS, push notifications, or multiple channels?"
    ],

    "test_cases": [

        {
            "id": "TC-01",
            "scenario":
                "A new user registers with valid information.",
            "expected":
                "A user account should be created successfully."
        },

        {
            "id": "TC-02",
            "scenario":
                "A customer searches for an available grocery product.",
            "expected":
                "Matching products should be displayed."
        },

        {
            "id": "TC-03",
            "scenario":
                "A customer adds a product and changes its quantity.",
            "expected":
                "The cart quantity and total price should update correctly."
        },

        {
            "id": "TC-04",
            "scenario":
                "A customer completes checkout with successful payment.",
            "expected":
                "The order should be created and confirmation should be displayed."
        },

        {
            "id": "TC-05",
            "scenario":
                "A customer opens tracking for an existing order.",
            "expected":
                "The current delivery status should be displayed."
        },

        {
            "id": "TC-06",
            "scenario":
                "Payment fails during checkout.",
            "expected":
                "The order should not be confirmed."
        }
    ],

    "technical_dependencies": [

        "User authentication and authorization",

        "Product and inventory database",

        "Shopping cart and order management backend",

        "Payment gateway API",

        "Delivery tracking service",

        "Notification service",

        "Web or mobile frontend"
    ]
}


# =========================================================
# GEMINI PROMPT
# =========================================================

def create_prompt(idea):

    return f"""
You are an AI Requirements Engineering Agent.

Analyze this software product idea:

{idea}

Return ONLY valid JSON using exactly this structure:

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
3. Generate Agile user stories.
4. Generate useful acceptance criteria.
5. Use MoSCoW prioritization.
6. Identify missing or ambiguous requirements.
7. Generate practical test cases.
8. Identify technical dependencies.
9. Keep everything concise.
10. Do not invent unnecessary features.
"""


# =========================================================
# GEMINI ANALYSIS
# =========================================================

def analyze_with_gemini(idea, key):

    client = genai.Client(
        api_key=key
    )

    prompt = create_prompt(
        idea
    )

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

            return json.loads(
                response.text
            )

        except Exception as e:

            last_error = e

            error_text = str(e)

            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
            ):

                if attempt < 2:

                    time.sleep(
                        2 ** attempt
                    )

                    continue

            raise last_error

    raise last_error


# =========================================================
# SUMMARY DASHBOARD
# =========================================================

def display_summary(data):

    functional = len(
        data.get(
            "functional_requirements",
            []
        )
    )

    non_functional = len(
        data.get(
            "non_functional_requirements",
            []
        )
    )

    stories = len(
        data.get(
            "user_stories",
            []
        )
    )

    priorities = len(
        data.get(
            "priorities",
            []
        )
    )

    gaps = len(
        data.get(
            "ambiguities",
            []
        )
    )

    tests = len(
        data.get(
            "test_cases",
            []
        )
    )

    dependencies = len(
        data.get(
            "technical_dependencies",
            []
        )
    )

    total = functional + non_functional

    st.subheader(
        "📊 Requirement Summary Dashboard"
    )

    st.caption(
        "AI-generated overview of the requirement analysis."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Total Requirements",
            total
        )

    with c2:
        st.metric(
            "Functional",
            functional
        )

    with c3:
        st.metric(
            "Non-Functional",
            non_functional
        )

    with c4:
        st.metric(
            "User Stories",
            stories
        )

    c5, c6, c7, c8 = st.columns(4)

    with c5:
        st.metric(
            "Prioritized",
            priorities
        )

    with c6:
        st.metric(
            "Gaps Detected",
            gaps
        )

    with c7:
        st.metric(
            "Test Cases",
            tests
        )

    with c8:
        st.metric(
            "Dependencies",
            dependencies
        )


# =========================================================
# TRACEABILITY MATRIX
# =========================================================

def display_traceability(data):

    st.subheader(
        "🔗 Requirement Traceability Matrix"
    )

    st.caption(
        "Requirement → User Story → Test Case"
    )

    requirements = data.get(
        "functional_requirements",
        []
    )

    stories = data.get(
        "user_stories",
        []
    )

    tests = data.get(
        "test_cases",
        []
    )

    if not requirements:

        st.info(
            "No functional requirements available."
        )

        return

    rows = []

    for i, requirement in enumerate(
        requirements,
        1
    ):

        # Match requirement to story
        if stories:

            story_index = (
                (i - 1) % len(stories)
            )

            story = stories[
                story_index
            ]

            story_id = (
                f"US-{story_index + 1:02d}"
            )

            story_text = story.get(
                "story",
                ""
            )

        else:

            story_id = "—"
            story_text = "Not generated"


        # Match requirement to test
        if tests:

            test_index = (
                (i - 1) % len(tests)
            )

            test = tests[
                test_index
            ]

            test_id = test.get(
                "id",
                f"TC-{test_index + 1:02d}"
            )

            test_scenario = test.get(
                "scenario",
                ""
            )

        else:

            test_id = "—"
            test_scenario = "Not generated"


        rows.append(
            {
                "Requirement":
                    f"FR-{i:02d}",

                "Requirement Description":
                    requirement,

                "User Story":
                    story_id,

                "Test Case":
                    test_id,

                "Test Scenario":
                    test_scenario
            }
        )

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "💡 Traceability connects requirements with "
        "development stories and validation tests."
    )


# =========================================================
# DISPLAY RESULTS
# =========================================================

def display_results(data):

    st.write("")

    # SUMMARY

    display_summary(
        data
    )

    st.divider()

    # TABS

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "📋 Requirements",
            "👤 User Stories",
            "⚡ Priorities",
            "🔎 Gaps",
            "🧪 Test Cases",
            "🔧 Technical",
            "🔗 Traceability"
        ]
    )


    # =====================================================
    # REQUIREMENTS
    # =====================================================

    with tab1:

        st.markdown(
            "### Functional Requirements"
        )

        for i, req in enumerate(
            data.get(
                "functional_requirements",
                []
            ),
            1
        ):

            with st.container(
                border=True
            ):

                st.write(
                    f"**FR-{i:02d}**"
                )

                st.write(req)


        st.markdown(
            "### Non-Functional Requirements"
        )

        for i, req in enumerate(
            data.get(
                "non_functional_requirements",
                []
            ),
            1
        ):

            with st.container(
                border=True
            ):

                st.write(
                    f"**NFR-{i:02d}**"
                )

                st.write(req)


    # =====================================================
    # USER STORIES
    # =====================================================

    with tab2:

        stories = data.get(
            "user_stories",
            []
        )

        if not stories:

            st.info(
                "No user stories generated."
            )

        for i, story in enumerate(
            stories,
            1
        ):

            with st.container(
                border=True
            ):

                st.markdown(
                    f"### 👤 User Story {i}"
                )

                st.write(
                    story.get(
                        "story",
                        ""
                    )
                )

                criteria = story.get(
                    "acceptance_criteria",
                    []
                )

                if criteria:

                    st.write(
                        "**Acceptance Criteria**"
                    )

                    for criterion in criteria:

                        st.write(
                            f"• {criterion}"
                        )


    # =====================================================
    # PRIORITIES
    # =====================================================

    with tab3:

        priorities = data.get(
            "priorities",
            []
        )

        for item in priorities:

            with st.container(
                border=True
            ):

                st.write(
                    f"**{item.get('requirement', 'Requirement')}**"
                )

                st.write(
                    f"Priority: **{item.get('priority', 'N/A')}**"
                )

                st.caption(
                    item.get(
                        "reason",
                        ""
                    )
                )


    # =====================================================
    # GAPS
    # =====================================================

    with tab4:

        ambiguities = data.get(
            "ambiguities",
            []
        )

        if not ambiguities:

            st.success(
                "✅ No major ambiguities detected."
            )

        for i, item in enumerate(
            ambiguities,
            1
        ):

            with st.container(
                border=True
            ):

                st.write(
                    f"🔎 **Gap {i}**"
                )

                st.write(item)


    # =====================================================
    # TEST CASES
    # =====================================================

    with tab5:

        test_cases = data.get(
            "test_cases",
            []
        )

        for test in test_cases:

            with st.container(
                border=True
            ):

                st.write(
                    f"### 🧪 {test.get('id', 'Test Case')}"
                )

                st.write(
                    f"**Scenario:** "
                    f"{test.get('scenario', '')}"
                )

                st.write(
                    f"**Expected:** "
                    f"{test.get('expected', '')}"
                )


    # =====================================================
    # TECHNICAL
    # =====================================================

    with tab6:

        dependencies = data.get(
            "technical_dependencies",
            []
        )

        for dependency in dependencies:

            st.write(
                f"🔧 {dependency}"
            )


    # =====================================================
    # TRACEABILITY
    # =====================================================

    with tab7:

        display_traceability(
            data
        )


    # =====================================================
    # DOWNLOAD
    # =====================================================

    st.divider()

    json_data = json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    )

    st.download_button(
        "📥 Download Requirements Report",
        data=json_data,
        file_name="reqpilot_requirements.json",
        mime="application/json",
        use_container_width=True
    )


# =========================================================
# ACTION BUTTONS
# =========================================================

st.write("")

col1, col2 = st.columns(2)

with col1:

    analyze = st.button(
        "⚡ Analyze Requirements",
        type="primary",
        use_container_width=True
    )

with col2:

    demo = st.button(
        "🎬 Demo Mode",
        use_container_width=True
    )


# =========================================================
# GEMINI ANALYZE
# =========================================================

if analyze:

    if not idea.strip():

        st.warning(
            "⚠️ Please enter a product idea first."
        )

    elif not api_key:

        st.error(
            "❌ Gemini API key is required for AI analysis."
        )

    else:

        with st.spinner(
            "🤖 Analyzing requirements..."
        ):

            try:

                result = analyze_with_gemini(
                    idea,
                    api_key
                )

                st.success(
                    "✅ Requirements generated successfully!"
                )

                display_results(
                    result
                )

            except Exception as e:

                st.error(
                    f"❌ AI analysis failed: {e}"
                )


# =========================================================
# PROPER DEMO MODE
# =========================================================

if demo:

    if preset == "QuickCart Grocery Platform":

        st.success(
            "🎬 Demo Mode activated — QuickCart Grocery Platform"
        )

        st.caption(
            "This is a pre-generated demo dataset. "
            "No Gemini API call is required."
        )

        display_results(
            demo_data
        )

    else:

        st.info(
            "🎬 For the hackathon demo, select "
            "**QuickCart Grocery Platform** from the "
            "Demo Preset and click Demo Mode."
        )


# =========================================================
# TECHNICAL CONTRIBUTION
# =========================================================

st.write("")

with st.container(border=True):

    st.subheader(
        "🧠 Technical Contribution"
    )

    st.write(
        "Our solution is not just a generic API wrapper. "
        "ReqPilot contributes through a structured multi-stage "
        "requirements analysis pipeline covering requirement "
        "classification, ambiguity detection, prioritization, "
        "user-story generation, test-case generation, and "
        "requirement traceability from a single project description."
    )


# =========================================================
# FOOTER
# =========================================================

st.write("")

st.caption(
    "🚀 ReqPilot • AI Requirements Engineering Agent • G14"
)
