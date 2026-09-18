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

    st.markdown("""
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
    """, unsafe_allow_html=True)

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
            "Student Learning Platform",
            "Hospital Appointment System"
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
""",

    "Hospital Appointment System": """
We want to build a hospital appointment system where patients can create
accounts, search doctors by specialization, view available slots, book
appointments, receive reminders, and view appointment history.
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

def create_demo(
    functional_requirements,
    non_functional_requirements,
    user_stories,
    priorities,
    ambiguities,
    test_cases,
    technical_dependencies
):

    return {

        "functional_requirements": functional_requirements,

        "non_functional_requirements": non_functional_requirements,

        "user_stories": user_stories,

        "priorities": priorities,

        "ambiguities": ambiguities,

        "test_cases": test_cases,

        "technical_dependencies": technical_dependencies
    }


# =========================================================
# 1. QUICKCART
# =========================================================

quickcart_demo = create_demo(

    [
        "Users should be able to create an account and securely log in.",
        "Users should be able to browse groceries by category and search for products.",
        "Users should be able to add products to a shopping cart and update quantities.",
        "Users should be able to place orders and make online payments.",
        "Users should be able to view order status and track delivery.",
        "The system should send order confirmation and delivery notifications."
    ],

    [
        "User payment and personal information must be securely protected.",
        "The application should provide fast response times.",
        "The system should remain available during high-demand periods.",
        "The application should support multiple concurrent users."
    ],

    [
        {
            "story": "As a customer, I want to search for groceries so that I can quickly find the products I need.",
            "acceptance_criteria": [
                "Given the user is on the product page, when they enter a product name, matching products should be displayed.",
                "Given no matching product exists, an appropriate message should be displayed."
            ]
        },
        {
            "story": "As a customer, I want to place an online order so that I can receive groceries at my preferred address.",
            "acceptance_criteria": [
                "Given the cart contains products, when payment succeeds, the order should be created.",
                "Given payment fails, the order should not be confirmed."
            ]
        },
        {
            "story": "As a customer, I want to track my order so that I know its current delivery status.",
            "acceptance_criteria": [
                "Given an order exists, the current delivery status should be displayed.",
                "The user should receive updates when the delivery status changes."
            ]
        }
    ],

    [
        {
            "requirement": "User registration and login",
            "priority": "Must Have",
            "reason": "Required for account and order management."
        },
        {
            "requirement": "Product search and browsing",
            "priority": "Must Have",
            "reason": "Customers need to find products."
        },
        {
            "requirement": "Shopping cart",
            "priority": "Must Have",
            "reason": "Required before checkout."
        },
        {
            "requirement": "Online payment",
            "priority": "Must Have",
            "reason": "Required to complete orders."
        },
        {
            "requirement": "Order tracking",
            "priority": "Should Have",
            "reason": "Improves delivery visibility."
        }
    ],

    [
        "Which payment methods should be supported?",
        "What delivery areas should be supported?",
        "What happens when a product becomes unavailable?",
        "Should users be able to cancel an order after payment?",
        "Should notifications use SMS, email, push notifications, or all three?"
    ],

    [
        {
            "id": "TC-01",
            "scenario": "User searches for an available grocery product.",
            "expected": "Matching products should be displayed."
        },
        {
            "id": "TC-02",
            "scenario": "User adds products to the cart.",
            "expected": "Cart quantity and total price should update correctly."
        },
        {
            "id": "TC-03",
            "scenario": "User completes checkout successfully.",
            "expected": "An order should be created."
        },
        {
            "id": "TC-04",
            "scenario": "Payment fails during checkout.",
            "expected": "The order should not be confirmed."
        },
        {
            "id": "TC-05",
            "scenario": "User opens order tracking.",
            "expected": "Current delivery status should be displayed."
        }
    ],

    [
        "User authentication",
        "Product and inventory database",
        "Shopping cart and order backend",
        "Payment gateway API",
        "Delivery tracking service",
        "Notification service",
        "Web or mobile frontend"
    ]
)


# =========================================================
# 2. AI FITNESS
# =========================================================

fitness_demo = create_demo(

    [
        "Users should be able to create fitness profiles.",
        "Users should be able to set fitness goals.",
        "The system should generate personalized workout plans.",
        "Users should be able to record completed workouts.",
        "Users should be able to view fitness progress.",
        "The system should provide activity-based recommendations."
    ],

    [
        "Fitness data should be securely stored.",
        "The platform should provide responsive performance.",
        "Recommendations should be generated consistently.",
        "The platform should support multiple concurrent users."
    ],

    [
        {
            "story": "As a user, I want to set fitness goals so that my workouts match my objectives.",
            "acceptance_criteria": [
                "The selected fitness goal should be saved.",
                "The goal should influence future recommendations."
            ]
        },
        {
            "story": "As a user, I want personalized workout plans so that I can follow a suitable routine.",
            "acceptance_criteria": [
                "Given a fitness goal exists, a suitable workout plan should be generated."
            ]
        }
    ],

    [
        {
            "requirement": "Fitness profile",
            "priority": "Must Have",
            "reason": "Required for personalization."
        },
        {
            "requirement": "Fitness goals",
            "priority": "Must Have",
            "reason": "Required for workout planning."
        },
        {
            "requirement": "Workout tracking",
            "priority": "Must Have",
            "reason": "Required for progress tracking."
        },
        {
            "requirement": "AI recommendations",
            "priority": "Should Have",
            "reason": "Enhances personalization."
        }
    ],

    [
        "Which fitness activities should be supported?",
        "What user information should be used for recommendations?",
        "How often should recommendations be updated?",
        "Should users be able to edit generated plans?"
    ],

    [
        {
            "id": "TC-01",
            "scenario": "User creates a fitness profile.",
            "expected": "Profile should be stored successfully."
        },
        {
            "id": "TC-02",
            "scenario": "User sets a fitness goal.",
            "expected": "Goal should be saved."
        },
        {
            "id": "TC-03",
            "scenario": "User requests a workout plan.",
            "expected": "A suitable workout plan should be generated."
        },
        {
            "id": "TC-04",
            "scenario": "User records a workout.",
            "expected": "Workout should appear in progress history."
        }
    ],

    [
        "User authentication",
        "Fitness profile database",
        "Workout recommendation engine",
        "Activity tracking module",
        "Backend API"
    ]
)


# =========================================================
# 3. EV CHARGING
# =========================================================

ev_demo = create_demo(

    [
        "Users should be able to find nearby EV charging stations.",
        "Users should be able to view station availability.",
        "Users should be able to reserve charging slots.",
        "Users should be able to make online payments.",
        "Users should receive charging completion notifications.",
        "Users should be able to view charging history."
    ],

    [
        "Location information should be handled securely.",
        "Station availability should be updated reliably.",
        "The platform should support multiple users.",
        "Payment information should be protected."
    ],

    [
        {
            "story": "As an EV owner, I want to find nearby charging stations so that I can plan my charging.",
            "acceptance_criteria": [
                "Nearby charging stations should be displayed.",
                "Station availability should be visible."
            ]
        },
        {
            "story": "As an EV owner, I want to reserve a charging slot so that I can charge my vehicle at a planned time.",
            "acceptance_criteria": [
                "Given a slot is available, the reservation should be created successfully."
            ]
        }
    ],

    [
        {
            "requirement": "Station search",
            "priority": "Must Have",
            "reason": "Users need to locate stations."
        },
        {
            "requirement": "Availability status",
            "priority": "Must Have",
            "reason": "Users need current station information."
        },
        {
            "requirement": "Slot reservation",
            "priority": "Must Have",
            "reason": "Reservation is a core workflow."
        },
        {
            "requirement": "Charging history",
            "priority": "Could Have",
            "reason": "Useful but not essential for basic charging."
        }
    ],

    [
        "Which charging connector types should be supported?",
        "How should station availability be updated?",
        "How long can a charging slot be reserved?",
        "Which payment methods should be supported?"
    ],

    [
        {
            "id": "TC-01",
            "scenario": "User searches for nearby charging stations.",
            "expected": "Nearby stations should be displayed."
        },
        {
            "id": "TC-02",
            "scenario": "User views station availability.",
            "expected": "Current available slots should be displayed."
        },
        {
            "id": "TC-03",
            "scenario": "User reserves an available slot.",
            "expected": "The slot should be reserved."
        },
        {
            "id": "TC-04",
            "scenario": "User completes payment.",
            "expected": "Payment status should be recorded."
        }
    ],

    [
        "Location or map API",
        "Charging station database",
        "Reservation backend",
        "Payment gateway",
        "Notification service",
        "Mobile frontend"
    ]
)


# =========================================================
# 4. STUDENT LEARNING
# =========================================================

student_demo = create_demo(

    [
        "Students should be able to create accounts.",
        "Students should be able to access courses.",
        "Students should be able to watch lessons.",
        "Students should be able to complete quizzes.",
        "Students should be able to track course progress.",
        "The system should provide learning recommendations."
    ],

    [
        "Student data should be securely stored.",
        "Lessons should load efficiently.",
        "The system should support multiple students.",
        "The platform should remain available during peak usage."
    ],

    [
        {
            "story": "As a student, I want to access courses so that I can learn new topics.",
            "acceptance_criteria": [
                "Available courses should be displayed to authenticated students.",
                "Students should be able to open a selected course."
            ]
        },
        {
            "story": "As a student, I want to track my progress so that I know how much of a course I have completed.",
            "acceptance_criteria": [
                "Completed lessons should update course progress.",
                "Progress percentage should be displayed."
            ]
        }
    ],

    [
        {
            "requirement": "Student account",
            "priority": "Must Have",
            "reason": "Required for learning progress."
        },
        {
            "requirement": "Course access",
            "priority": "Must Have",
            "reason": "Core platform functionality."
        },
        {
            "requirement": "Quizzes",
            "priority": "Should Have",
            "reason": "Helps evaluate learning."
        },
        {
            "requirement": "Personalized recommendations",
            "priority": "Could Have",
            "reason": "Improves personalization."
        }
    ],

    [
        "Which subjects should be supported?",
        "Should courses require payment?",
        "What quiz types should be supported?",
        "How should recommendations be generated?"
    ],

    [
        {
            "id": "TC-01",
            "scenario": "Student logs into the platform.",
            "expected": "Student should be authenticated."
        },
        {
            "id": "TC-02",
            "scenario": "Student opens a course.",
            "expected": "Available lessons should be displayed."
        },
        {
            "id": "TC-03",
            "scenario": "Student completes a lesson.",
            "expected": "Course progress should update."
        },
        {
            "id": "TC-04",
            "scenario": "Student completes a quiz.",
            "expected": "Quiz result should be recorded."
        }
    ],

    [
        "Authentication system",
        "Course database",
        "Video/content delivery",
        "Quiz engine",
        "Progress tracking backend",
        "Recommendation engine"
    ]
)


# =========================================================
# 5. HOSPITAL
# =========================================================

hospital_demo = create_demo(

    [
        "Patients should be able to create accounts.",
        "Patients should be able to search doctors by specialization.",
        "Patients should be able to view available appointment slots.",
        "Patients should be able to book appointments.",
        "Patients should receive appointment reminders.",
        "Patients should be able to view appointment history."
    ],

    [
        "Patient information must be securely protected.",
        "Appointment availability should remain consistent.",
        "The system should support concurrent booking requests.",
        "The platform should provide reliable access."
    ],

    [
        {
            "story": "As a patient, I want to search doctors by specialization so that I can find a suitable doctor.",
            "acceptance_criteria": [
                "When a specialization is selected, matching doctors should be displayed."
            ]
        },
        {
            "story": "As a patient, I want to book an appointment so that I can consult a doctor.",
            "acceptance_criteria": [
                "Given an available slot, the appointment should be created.",
                "The booked slot should no longer be available."
            ]
        }
    ],

    [
        {
            "requirement": "Patient registration",
            "priority": "Must Have",
            "reason": "Required for appointment management."
        },
        {
            "requirement": "Doctor search",
            "priority": "Must Have",
            "reason": "Patients need to find doctors."
        },
        {
            "requirement": "Appointment booking",
            "priority": "Must Have",
            "reason": "Core system workflow."
        },
        {
            "requirement": "Appointment reminders",
            "priority": "Should Have",
            "reason": "Helps patients manage appointments."
        }
    ],

    [
        "Which doctor specializations should be supported?",
        "What patient information is required?",
        "Can patients cancel or reschedule appointments?",
        "Which reminder channels should be supported?"
    ],

    [
        {
            "id": "TC-01",
            "scenario": "Patient searches for a doctor.",
            "expected": "Matching doctors should be displayed."
        },
        {
            "id": "TC-02",
            "scenario": "Patient books an available appointment.",
            "expected": "Appointment should be created successfully."
        },
        {
            "id": "TC-03",
            "scenario": "Two users attempt to book the same slot.",
            "expected": "Only one booking should succeed."
        },
        {
            "id": "TC-04",
            "scenario": "Patient views appointment history.",
            "expected": "Previous appointments should be displayed."
        }
    ],

    [
        "Patient database",
        "Doctor database",
        "Appointment scheduling backend",
        "Authentication system",
        "Notification service",
        "Web or mobile frontend"
    ]
)


# =========================================================
# DEMO DATA MAP
# =========================================================

demo_data_map = {

    "QuickCart Grocery Platform": quickcart_demo,

    "AI Fitness Platform": fitness_demo,

    "EV Charging Platform": ev_demo,

    "Student Learning Platform": student_demo,

    "Hospital Appointment System": hospital_demo
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
4. Include acceptance criteria.
5. Prioritize requirements using MoSCoW:
   Must Have, Should Have, Could Have, Won't Have.
6. Identify missing or ambiguous requirements.
7. Generate practical test cases.
8. Identify realistic technical dependencies.
9. Do not invent unnecessary features.
10. Keep the output concise.
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
# DISPLAY RESULTS
# =========================================================

def display_results(data):

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


    # =====================================================
    # REQUIREMENTS
    # =====================================================

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


    # =====================================================
    # USER STORIES
    # =====================================================

    with tab2:

        stories = data.get("user_stories", [])

        for i, story in enumerate(stories, 1):

            with st.container(border=True):

                st.markdown(f"### 👤 User Story {i}")

                st.write(
                    story.get("story", "")
                )

                criteria = story.get(
                    "acceptance_criteria",
                    []
                )

                if criteria:

                    st.write("**Acceptance Criteria**")

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

            with st.container(border=True):

                st.write(
                    f"**{item.get('requirement', 'Requirement')}**"
                )

                st.write(
                    f"Priority: "
                    f"**{item.get('priority', 'N/A')}**"
                )

                st.caption(
                    item.get("reason", "")
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


    # =====================================================
    # TEST CASES
    # =====================================================

    with tab5:

        test_cases = data.get(
            "test_cases",
            []
        )

        for test in test_cases:

            with st.container(border=True):

                st.write(
                    f"### 🧪 "
                    f"{test.get('id', 'Test Case')}"
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

            with st.container(border=True):

                st.write(
                    f"🔧 {dependency}"
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
# ANALYZE REQUIREMENTS
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
# DEMO MODE
# =========================================================

if demo:

    if preset == "Custom Idea":

        st.info(
            "💡 Custom Idea selected. "
            "Enter your own idea and use "
            "⚡ Analyze Requirements."
        )

    elif preset in demo_data_map:

        st.success(
            f"🎬 Demo Mode activated — {preset}"
        )

        st.caption(
            "Pre-generated demo data • No API call required"
        )

        display_results(
            demo_data_map[preset]
        )


# =========================================================
# FOOTER
# =========================================================

st.write("")

st.caption(
    "ReqPilot • G14 • AI Requirements Engineering Agent"
)
