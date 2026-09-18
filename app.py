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
# GLASS UI CSS
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

code {
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOGIN
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding-top:80px;
            padding-bottom:25px;
        ">
            <div style="font-size:60px;">🚀</div>
            <h1>ReqPilot</h1>
            <p style="font-size:18px;">
                AI Requirements Engineering Agent
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:

        with st.container(border=True):

            st.subheader("🔐 Login")

            username = st.text_input(
                "👤 Username",
                placeholder="Enter username"
            )

            password = st.text_input(
                "🔒 Password",
                type="password",
                placeholder="Enter password"
            )

            if st.button(
                "🚀 Login",
                type="primary",
                use_container_width=True
            ):

                if username == "reqpilot" and password == "reqpilot123":

                    st.session_state.logged_in = True

                    st.success("Login successful! 🎉")

                    time.sleep(0.5)

                    st.rerun()

                else:

                    st.error("❌ Invalid username or password.")

            st.caption("Demo Login: reqpilot / reqpilot123")

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🚀 ReqPilot")
    st.caption("AI Requirements Engineering Agent")

    st.divider()

    st.subheader("🔑 AI Connection")

    api_key = None

    try:

        api_key = st.secrets["GEMINI_API_KEY"]

        st.success("API Key Loaded from Secrets")

    except Exception:

        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="Enter API key"
        )

    st.divider()

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

    st.subheader("⚙️ Pipeline")

    st.write("💡 Raw Idea")
    st.write("🧩 Requirement Extraction")
    st.write("🏷️ Classification")
    st.write("⚡ Prioritization")
    st.write("🔎 Gap Detection")
    st.write("🧪 Test Generation")

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):

        st.session_state.logged_in = False

        st.rerun()

    st.divider()

    st.caption("G14 • AI Requirements Engineering Agent")


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

    st.caption("G14 • AI REQUIREMENTS ENGINEERING AGENT")

    st.title("🚀 ReqPilot")

    st.write(
        "Turn an informal product idea into structured, development-ready "
        "software requirements using AI."
    )

    st.write(
        "Requirements • User Stories • Priorities • Gaps • Test Cases • Dependencies"
    )


# =========================================================
# INPUT SECTION
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
            "Example: We want to build an online grocery delivery "
            "platform where users can..."
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

st.subheader("🔄 Requirement Intelligence Pipeline")

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

            st.markdown(f"### {icon}")

            st.write(f"**{title}**")

            st.caption(subtitle)


# =========================================================
# DEMO DATA
# =========================================================

demo_data = {

    "functional_requirements": [

        "Users should be able to create an account and securely log in.",

        "Users should be able to browse groceries by category and search for products.",

        "Users should be able to add products to a shopping cart and update quantities.",

        "Users should be able to place orders and make online payments.",

        "Users should be able to view their order status and track delivery.",

        "The system should send notifications for order confirmation and delivery updates."
    ],

    "non_functional_requirements": [

        "User payment and personal information must be securely protected.",

        "The application should provide fast response times during normal usage.",

        "The system should remain available during high-demand periods.",

        "The application should support multiple users placing orders simultaneously."
    ],

    "user_stories": [

        {
            "story":
                "As a customer, I want to search for groceries so that I can quickly find the products I need.",

            "acceptance_criteria": [

                "Given the user is on the product page, when they enter a product name, then matching products should be displayed.",

                "Given no matching product exists, when the user searches, then a suitable message should be displayed."
            ]
        },

        {
            "story":
                "As a customer, I want to place an online order so that I can receive groceries at my preferred address.",

            "acceptance_criteria": [

                "Given the cart contains products, when the user confirms the order and payment succeeds, then the order should be created.",

                "Given payment fails, when the user attempts to place the order, then the order should not be confirmed."
            ]
        },

        {
            "story":
                "As a customer, I want to track my order so that I know its current delivery status.",

            "acceptance_criteria": [

                "Given an order has been placed, when the user opens order tracking, then the current order status should be displayed.",

                "The user should receive updates when the delivery status changes."
            ]
        }
    ],

    "priorities": [

        {
            "requirement": "User registration and login",
            "priority": "Must Have",
            "reason":
                "Users need secure accounts to manage orders and personal information."
        },

        {
            "requirement": "Product search and browsing",
            "priority": "Must Have",
            "reason":
                "Customers need to find products before placing an order."
        },

        {
            "requirement": "Shopping cart",
            "priority": "Must Have",
            "reason":
                "Customers need to select and manage products before checkout."
        },

        {
            "requirement": "Online payment",
            "priority": "Must Have",
            "reason":
                "Payment is required to complete an online order."
        },

        {
            "requirement": "Order tracking",
            "priority": "Should Have",
            "reason":
                "Tracking improves delivery visibility and customer experience."
        },

        {
            "requirement": "Personalized product recommendations",
            "priority": "Could Have",
            "reason":
                "Recommendations can improve product discovery but are not required for the core ordering flow."
        }
    ],

    "ambiguities": [

        "Which payment methods should be supported?",

        "What delivery areas and geographical locations should be supported?",

        "What happens when a product becomes unavailable after the user adds it to the cart?",

        "Should users be able to cancel an order after payment?",

        "What is the expected delivery time?",

        "Should notifications be sent through SMS, email, push notifications, or all three?"
    ],

    "test_cases": [

        {
            "id": "TC-01",
            "scenario": "User searches for an available grocery product.",
            "expected":
                "Matching products should be displayed with product name, price, and availability."
        },

        {
            "id": "TC-02",
            "scenario":
                "User adds products to the cart and changes the quantity.",
            "expected":
                "Cart quantity and total price should update correctly."
        },

        {
            "id": "TC-03",
            "scenario":
                "User completes checkout with a successful payment.",
            "expected":
                "The order should be created and an order confirmation should be displayed."
        },

        {
            "id": "TC-04",
            "scenario":
                "Payment fails during checkout.",
            "expected":
                "The order should not be confirmed and the user should receive an appropriate error message."
        },

        {
            "id": "TC-05",
            "scenario":
                "User opens tracking for an existing order.",
            "expected":
                "The current delivery status should be displayed."
        }
    ],

    "technical_dependencies": [

        "User authentication and authorization",

        "Product and inventory database",

        "Shopping cart and order management backend",

        "Payment gateway API",

        "Delivery and order tracking service",

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

Analyze the following software product idea:

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

1. Extract clear functional requirements.
2. Extract realistic non-functional requirements.
3. Generate Agile-style user stories.
4. Include Given/When/Then style acceptance criteria where useful.
5. Prioritize requirements using MoSCoW:
   Must Have, Should Have, Could Have, Won't Have.
6. Identify missing or ambiguous requirements.
7. Generate practical test cases.
8. Identify realistic technical dependencies.
9. Do not invent unnecessary features.
10. Keep the output concise and suitable for a software development team.
"""


# =========================================================
# GEMINI ANALYSIS
# =========================================================

def analyze_with_gemini(idea, key):

    client = genai.Client(api_key=key)

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

            return json.loads(response.text)

        except Exception as e:

            last_error = e

            error_text = str(e)

            if "503" in error_text or "UNAVAILABLE" in error_text:

                if attempt < 2:

                    time.sleep(2 ** attempt)

                    continue

            raise last_error

    raise last_error


# =========================================================
# SUMMARY DASHBOARD
# =========================================================

def display_summary(data):

    fr_count = len(
        data.get("functional_requirements", [])
    )

    nfr_count = len(
        data.get("non_functional_requirements", [])
    )

    story_count = len(
        data.get("user_stories", [])
    )

    gap_count = len(
        data.get("ambiguities", [])
    )

    test_count = len(
        data.get("test_cases", [])
    )

    dependency_count = len(
        data.get("technical_dependencies", [])
    )

    st.subheader("📊 Requirement Summary")

    s1, s2, s3 = st.columns(3)

    with s1:
        st.metric(
            "Functional Requirements",
            fr_count
        )

    with s2:
        st.metric(
            "Non-Functional Requirements",
            nfr_count
        )

    with s3:
        st.metric(
            "User Stories",
            story_count
        )

    s4, s5, s6 = st.columns(3)

    with s4:
        st.metric(
            "Ambiguities / Gaps",
            gap_count
        )

    with s5:
        st.metric(
            "Test Cases",
            test_count
        )

    with s6:
        st.metric(
            "Dependencies",
            dependency_count
        )


# =========================================================
# TRACEABILITY MATRIX
# =========================================================

def display_traceability(data):

    st.subheader("🔗 Requirement Traceability Matrix")

    functional = data.get(
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

    max_rows = max(
        len(functional),
        len(stories),
        len(tests)
    )

    if max_rows == 0:

        st.info(
            "No requirements available for traceability."
        )

        return

    rows = []

    for i in range(max_rows):

        requirement_id = (
            f"FR-{i + 1:02d}"
            if i < len(functional)
            else "-"
        )

        requirement = (
            functional[i]
            if i < len(functional)
            else "-"
        )

        story_id = (
            f"US-{i + 1:02d}"
            if i < len(stories)
            else "-"
        )

        story = (
            stories[i].get("story", "")
            if i < len(stories)
            else "-"
        )

        test_id = (
            tests[i].get("id", f"TC-{i + 1:02d}")
            if i < len(tests)
            else "-"
        )

        rows.append({
            "Requirement": requirement_id,
            "Requirement Description": requirement,
            "User Story": story_id,
            "User Story Description": story,
            "Test Case": test_id
        })

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# DOWNLOAD REPORT
# =========================================================

def create_report(data):

    report = []

    report.append("REQPILOT - AI REQUIREMENTS ENGINEERING REPORT")
    report.append("=" * 60)
    report.append("")

    report.append("FUNCTIONAL REQUIREMENTS")
    report.append("-" * 30)

    for i, req in enumerate(
        data.get("functional_requirements", []),
        1
    ):
        report.append(
            f"FR-{i:02d}: {req}"
        )

    report.append("")

    report.append("NON-FUNCTIONAL REQUIREMENTS")
    report.append("-" * 30)

    for i, req in enumerate(
        data.get("non_functional_requirements", []),
        1
    ):
        report.append(
            f"NFR-{i:02d}: {req}"
        )

    report.append("")

    report.append("USER STORIES")
    report.append("-" * 30)

    for i, story in enumerate(
        data.get("user_stories", []),
        1
    ):

        report.append(
            f"US-{i:02d}: {story.get('story', '')}"
        )

        for criterion in story.get(
            "acceptance_criteria",
            []
        ):

            report.append(
                f"  - {criterion}"
            )

    report.append("")

    report.append("PRIORITIES")
    report.append("-" * 30)

    for item in data.get("priorities", []):

        report.append(
            f"{item.get('requirement', '')} "
            f"→ {item.get('priority', '')}"
        )

        report.append(
            f"Reason: {item.get('reason', '')}"
        )

    report.append("")

    report.append("AMBIGUITIES / GAPS")
    report.append("-" * 30)

    for item in data.get(
        "ambiguities",
        []
    ):

        report.append(
            f"- {item}"
        )

    report.append("")

    report.append("TEST CASES")
    report.append("-" * 30)

    for test in data.get(
        "test_cases",
        []
    ):

        report.append(
            f"{test.get('id', '')}: "
            f"{test.get('scenario', '')}"
        )

        report.append(
            f"Expected: {test.get('expected', '')}"
        )

    report.append("")

    report.append("TECHNICAL DEPENDENCIES")
    report.append("-" * 30)

    for dependency in data.get(
        "technical_dependencies",
        []
    ):

        report.append(
            f"- {dependency}"
        )

    return "\n".join(report)


# =========================================================
# DISPLAY RESULTS
# =========================================================

def display_results(data):

    st.write("")

    display_summary(data)

    st.write("")

    display_traceability(data)

    st.write("")

    st.subheader("📊 Generated Requirements")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "📋 Requirements",
            "👤 User Stories",
            "⚡ Priorities",
            "🔎 Gaps",
            "🧪 Test Cases",
            "🔧 Technical"
        ]
    )


    # -----------------------------------------------------
    # REQUIREMENTS
    # -----------------------------------------------------

    with tab1:

        st.markdown("### Functional Requirements")

        for i, req in enumerate(
            data.get("functional_requirements", []),
            1
        ):

            with st.container(border=True):

                st.write(f"**FR-{i:02d}**")

                st.write(req)


        st.markdown("### Non-Functional Requirements")

        for i, req in enumerate(
            data.get("non_functional_requirements", []),
            1
        ):

            with st.container(border=True):

                st.write(f"**NFR-{i:02d}**")

                st.write(req)


    # -----------------------------------------------------
    # USER STORIES
    # -----------------------------------------------------

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

            with st.container(border=True):

                st.markdown(
                    f"### 👤 User Story {i}"
                )

                st.write(
                    story.get("story", "")
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


    # -----------------------------------------------------
    # PRIORITIES
    # -----------------------------------------------------

    with tab3:

        priorities = data.get(
            "priorities",
            []
        )

        for item in priorities:

            with st.container(border=True):

                st.write(
                    f"**{item.get('requirement', 'Requirement')}**"
                )

                st.write(
                    f"Priority: **{item.get('priority', 'N/A')}**"
                )

                st.caption(
                    item.get('reason', '')
                )


    # -----------------------------------------------------
    # GAPS
    # -----------------------------------------------------

    with tab4:

        ambiguities = data.get(
            "ambiguities",
            []
        )

        if not ambiguities:

            st.success(
                "No major ambiguities detected."
            )

        else:

            for i, item in enumerate(
                ambiguities,
                1
            ):

                with st.container(border=True):

                    st.write(
                        f"🔎 **Gap {i}**"
                    )

                    st.write(item)


    # -----------------------------------------------------
    # TEST CASES
    # -----------------------------------------------------

    with tab5:

        test_cases = data.get(
            "test_cases",
            []
        )

        for test in test_cases:

            with st.container(border=True):

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


    # -----------------------------------------------------
    # TECHNICAL
    # -----------------------------------------------------

    with tab6:

        dependencies = data.get(
            "technical_dependencies",
            []
        )

        for dependency in dependencies:

            with st.container(border=True):

                st.write(
                    f"🔧 {dependency}"
                )


    # =====================================================
    # DOWNLOAD
    # =====================================================

    st.write("")

    st.subheader("📥 Export")

    report = create_report(data)

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "📥 Download Report",
            data=report,
            file_name="reqpilot_requirements_report.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:

        st.download_button(
            "📦 Download JSON",
            data=json.dumps(
                data,
                indent=4
            ),
            file_name="reqpilot_requirements.json",
            mime="application/json",
            use_container_width=True
        )


# =========================================================
# ACTION BUTTONS
# =========================================================

st.write("")

col1, col2 = st.columns(2)


# =========================================================
# LIVE GEMINI ANALYSIS
# =========================================================

with col1:

    analyze = st.button(
        "⚡ Analyze Requirements",
        type="primary",
        use_container_width=True
    )


# =========================================================
# DEMO MODE
# =========================================================

with col2:

    demo = st.button(
        "🎬 Demo Mode",
        use_container_width=True
    )


# =========================================================
# BUTTON ACTIONS
# =========================================================

if analyze:

    if not idea.strip():

        st.warning(
            "⚠️ Please enter a product idea first."
        )

    elif not api_key:

        st.error(
            "🔑 Gemini API key is required for live analysis."
        )

    else:

        with st.spinner(
            "🤖 ReqPilot is analyzing your requirements..."
        ):

            try:

                result = analyze_with_gemini(
                    idea,
                    api_key
                )

                st.success(
                    "✅ Requirements generated successfully!"
                )

                display_results(result)

            except Exception as e:

                st.error(
                    f"❌ Gemini API Error: {e}"
                )


# =========================================================
# DEMO ACTION
# =========================================================

if demo:

    if preset == "QuickCart Grocery Platform":

        st.success(
            "🎬 Demo Mode activated — QuickCart Grocery Platform"
        )

        st.caption(
            "Pre-generated demo data is being displayed."
        )

        display_results(demo_data)

    else:

        st.info(
            "🎬 For the hackathon demo, select "
            "QuickCart Grocery Platform from the Demo Preset "
            "and click Demo Mode."
        )


# =========================================================
# TECHNICAL CONTRIBUTION
# =========================================================

st.write("")

with st.container(border=True):

    st.subheader("🧠 Technical Contribution")

    st.write(
        "Our solution is not just a generic API wrapper. "
        "We contribute through structured multi-stage requirement analysis, "
        "including requirement classification, ambiguity detection, "
        "prioritization, user-story generation, and test-case generation "
        "from a single project description."
    )


# =========================================================
# FOOTER
# =========================================================

st.write("")

st.caption(
    "ReqPilot • G14 • AI Requirements Engineering Agent"
)
