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
            "Student Learning Platform",
            "Hospital Appointment System",
            "Smart Hotel Booking Platform",
            "Ride Booking Platform",
            "Job Portal",
            "Online Exam Platform"
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
""",

    "Hospital Appointment System": """
We want to build a hospital appointment system where patients can create
accounts, search doctors by specialization, view available slots, book
appointments, receive reminders, and view appointment history.
""",

    "Smart Hotel Booking Platform": """
We want to build a smart hotel booking platform where users can search
hotels, view room availability, compare room options, make reservations,
complete online payments, and receive booking confirmations.
""",

    "Ride Booking Platform": """
We want to build a ride booking platform where users can select pickup and
drop locations, request rides, view estimated fares, track drivers,
complete payments, and rate completed rides.
""",

    "Job Portal": """
We want to build a job portal where job seekers can create profiles,
search jobs, filter opportunities, upload resumes, apply for jobs, and
track application status. Employers should be able to post jobs and review
applications.
""",

    "Online Exam Platform": """
We want to build an online exam platform where students can register for
exams, view instructions, answer questions, submit exams, and receive
results. Administrators should be able to create exams and manage questions.
"""
}


# =========================================================
# DEMO DATA GENERATOR
# =========================================================

def make_demo(
    fr,
    nfr,
    stories,
    priorities,
    ambiguities,
    tests,
    dependencies
):

    return {

        "functional_requirements": fr,

        "non_functional_requirements": nfr,

        "user_stories": stories,

        "priorities": priorities,

        "ambiguities": ambiguities,

        "test_cases": tests,

        "technical_dependencies": dependencies
    }


# =========================================================
# QUICKCART DEMO
# =========================================================

quickcart_data = make_demo(

    [
        "Users should be able to create an account and securely log in.",
        "Users should be able to browse groceries by category and search for products.",
        "Users should be able to add products to a shopping cart and update quantities.",
        "Users should be able to place orders and make online payments.",
        "Users should be able to view their order status and track delivery.",
        "The system should send notifications for order confirmation and delivery updates."
    ],

    [
        "User payment and personal information must be securely protected.",
        "The application should provide fast response times during normal usage.",
        "The system should remain available during high-demand periods.",
        "The application should support multiple users placing orders simultaneously."
    ],

    [
        {
            "story": "As a customer, I want to search for groceries so that I can quickly find the products I need.",
            "acceptance_criteria": [
                "Given the user is on the product page, when they enter a product name, then matching products should be displayed.",
                "Given no matching product exists, when the user searches, then a suitable message should be displayed."
            ]
        },
        {
            "story": "As a customer, I want to place an online order so that I can receive groceries at my preferred address.",
            "acceptance_criteria": [
                "Given the cart contains products, when the user confirms the order and payment succeeds, then the order should be created.",
                "Given payment fails, when the user attempts to place the order, then the order should not be confirmed."
            ]
        },
        {
            "story": "As a customer, I want to track my order so that I know its current delivery status.",
            "acceptance_criteria": [
                "Given an order has been placed, when the user opens order tracking, then the current order status should be displayed.",
                "The user should receive updates when the delivery status changes."
            ]
        }
    ],

    [
        {
            "requirement": "User registration and login",
            "priority": "Must Have",
            "reason": "Users need secure accounts to manage orders and personal information."
        },
        {
            "requirement": "Product search and browsing",
            "priority": "Must Have",
            "reason": "Customers need to find products before placing an order."
        },
        {
            "requirement": "Shopping cart",
            "priority": "Must Have",
            "reason": "Customers need to select and manage products before checkout."
        },
        {
            "requirement": "Online payment",
            "priority": "Must Have",
            "reason": "Payment is required to complete an online order."
        },
        {
            "requirement": "Order tracking",
            "priority": "Should Have",
            "reason": "Tracking improves delivery visibility and customer experience."
        },
        {
            "requirement": "Personalized product recommendations",
            "priority": "Could Have",
            "reason": "Recommendations can improve product discovery but are not required for the core ordering flow."
        }
    ],

    [
        "Which payment methods should be supported?",
        "What delivery areas and geographical locations should be supported?",
        "What happens when a product becomes unavailable after the user adds it to the cart?",
        "Should users be able to cancel an order after payment?",
        "What is the expected delivery time?",
        "Should notifications be sent through SMS, email, push notifications, or all three?"
    ],

    [
        {
            "id": "TC-01",
            "scenario": "User searches for an available grocery product.",
            "expected": "Matching products should be displayed with product name, price, and availability."
        },
        {
            "id": "TC-02",
            "scenario": "User adds products to the cart and changes the quantity.",
            "expected": "Cart quantity and total price should update correctly."
        },
        {
            "id": "TC-03",
            "scenario": "User completes checkout with a successful payment.",
            "expected": "The order should be created and an order confirmation should be displayed."
        },
        {
            "id": "TC-04",
            "scenario": "Payment fails during checkout.",
            "expected": "The order should not be confirmed and the user should receive an appropriate error message."
        },
        {
            "id": "TC-05",
            "scenario": "User opens tracking for an existing order.",
            "expected": "The current delivery status should be displayed."
        }
    ],

    [
        "User authentication and authorization",
        "Product and inventory database",
        "Shopping cart and order management backend",
        "Payment gateway API",
        "Delivery and order tracking service",
        "Notification service",
        "Web or mobile frontend"
    ]
)


# =========================================================
# AI FITNESS DEMO
# =========================================================

fitness_data = make_demo(

    [
        "Users should be able to create and manage fitness profiles.",
        "Users should be able to define fitness goals.",
        "The system should generate personalized workout plans.",
        "Users should be able to record completed workouts.",
        "Users should be able to view fitness progress.",
        "The system should provide recommendations based on recorded activity."
    ],

    [
        "Personal fitness data should be securely stored.",
        "The platform should provide responsive performance.",
        "The recommendation system should provide consistent results.",
        "The platform should support multiple concurrent users."
    ],

    [
        {
            "story": "As a user, I want to set fitness goals so that my workouts match my objectives.",
            "acceptance_criteria": [
                "Given a user profile exists, when a fitness goal is selected, then the goal should be saved.",
                "The selected goal should influence future workout recommendations."
            ]
        },
        {
            "story": "As a user, I want personalized workouts so that I can follow a suitable training plan.",
            "acceptance_criteria": [
                "Given a fitness goal exists, when the user requests a workout plan, then a suitable plan should be generated."
            ]
        }
    ],

    [
        {
            "requirement": "User profile",
            "priority": "Must Have",
            "reason": "The system needs user information to personalize fitness features."
        },
        {
            "requirement": "Fitness goals",
            "priority": "Must Have",
            "reason": "Goals are required for personalized planning."
        },
        {
            "requirement": "Workout tracking",
            "priority": "Must Have",
            "reason": "Tracking provides progress information."
        },
        {
            "requirement": "AI recommendations",
            "priority": "Should Have",
            "reason": "Recommendations enhance personalization."
        }
    ],

    [
        "Which fitness activities should be supported?",
        "What information should be used for personalization?",
        "How frequently should recommendations be updated?",
        "Should users be able to edit generated workout plans?"
    ],

    [
        {
            "id": "TC-01",
            "scenario": "User creates a fitness profile.",
            "expected": "Profile information should be stored successfully."
        },
        {
            "id": "TC-02",
            "scenario": "User sets a fitness goal.",
            "expected": "The selected goal should be saved."
        },
        {
            "id": "TC-03",
            "scenario": "User requests a personalized workout.",
            "expected": "A workout plan relevant to the selected goal should be generated."
        },
        {
            "id": "TC-04",
            "scenario": "User records a completed workout.",
            "expected": "The workout should appear in progress history."
        }
    ],

    [
        "User authentication",
        "Fitness profile database",
        "Workout recommendation engine",
        "Activity tracking module",
        "Backend API",
        "Web or mobile frontend"
    ]
)


# =========================================================
# EV CHARGING DEMO
# =========================================================

ev_data = make_demo(

    [
        "Users should be able to search for nearby EV charging stations.",
        "Users should be able to view charging station availability.",
        "Users should be able to reserve an available charging slot.",
        "Users should be able to make online payments.",
        "Users should receive charging completion notifications.",
        "Users should be able to view charging history."
    ],

    [
        "Location information should be handled securely.",
        "Station availability should be updated reliably.",
        "The platform should support multiple users simultaneously.",
        "Payment information should be securely protected."
    ],

    [
        {
            "story": "As an EV owner, I want to find nearby charging stations so that I can plan my charging.",
            "acceptance_criteria": [
                "Given location access is available, when the user searches for stations, then nearby stations should be displayed.",
                "Station availability should be visible."
            ]
        },
        {
            "story": "As an EV owner, I want to reserve a charging slot so that I can charge my vehicle at a planned time.",
            "acceptance_criteria": [
                "Given a slot is available, when the user confirms a reservation, then the slot should be reserved."
            ]
        }
    ],

    [
        {
            "requirement": "Station search",
            "priority": "Must Have",
            "reason": "Users need to locate charging stations."
        },
        {
            "requirement": "Availability status",
            "priority": "Must Have",
            "reason": "Users need current station information."
        },
        {
            "requirement": "Slot reservation",
            "priority": "Must Have",
            "reason": "Reservations are part of the core workflow."
        },
        {
            "requirement": "Charging history",
            "priority": "Could Have",
            "reason": "History is useful but not required for basic charging."
        }
    ],

    [
        "Which charging connector types should be supported?",
        "How should station availability be updated?",
        "How long can a user reserve a charging slot?",
        "What payment methods should be supported?"
    ],

    [
        {
            "id": "TC-01",
            "scenario": "User searches for nearby stations.",
            "expected": "Nearby charging stations should be displayed."
        },
        {
            "id": "TC-02",
            "scenario": "User views a station with available slots.",
            "expected": "Current slot availability should be displayed."
        },
        {
            "id": "TC-03",
            "scenario": "User reserves an available slot.",
            "expected": "The selected slot should be reserved successfully."
        },
        {
            "id": "TC-04",
            "scenario": "User completes payment.",
            "expected": "Payment status should be recorded successfully."
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
# STUDENT LEARNING DEMO
# =========================================================

student_data = make_demo(

    [
        "Students should be able to create accounts.",
        "Students should be able to access available courses.",
        "Students should be able to watch lessons.",
        "Students should be able to complete quizzes.",
        "Students should be able to track course progress.",
        "The system should provide personalized learning recommendations."
    ],

    [
        "Student data should be securely stored.",
        "Lessons should load efficiently.",
        "The system should support multiple students simultaneously.",
        "The platform should remain available during peak usage."
    ],

    [
        {
            "story": "As a student, I want to access courses so that I can learn new topics.",
            "acceptance_criteria": [
                "Given a valid account, when the student opens the course catalog, then available courses should be displayed."
            ]
        },
        {
            "story": "As a student, I want to track my progress so that I know how much of a course I have completed.",
            "acceptance_criteria": [
                "Completed lessons should update the student's progress.",
                "The progress percentage should be displayed."
            ]
        }
    ],

    [
        {
            "requirement": "Student account",
            "priority": "Must Have",
            "reason": "Students need accounts to track their learning."
        },
        {
            "requirement": "Course access",
            "priority": "Must Have",
            "reason": "Course content is the core platform feature."
        },
        {
            "requirement": "Quizzes",
            "priority": "Should Have",
            "reason": "Quizzes help evaluate learning."
        },
        {
            "requirement": "Personalized recommendations",
            "priority": "Could Have",
            "reason": "Recommendations improve personalization."
        }
    ],

    [
        "Which course subjects should be supported?",
        "Should courses require payment?",
        "What types of quizzes should be available?",
        "How should recommendations be generated?"
    ],

    [
        {
            "id": "TC-01",
            "scenario": "Student logs into the platform.",
            "expected": "The student should be authenticated successfully."
        },
        {
            "id": "TC-02",
            "scenario": "Student opens a course.",
            "expected": "Available lessons should be displayed."
        },
        {
            "id": "TC-03",
            "scenario": "Student completes a lesson.",
            "expected": "Course progress should be updated."
        },
        {
            "id": "TC-04",
            "scenario": "Student submits a quiz.",
            "expected": "The quiz result should be recorded."
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
# HOSPITAL DEMO
# =========================================================

hospital_data = make_demo(

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
            "story": "As a patient, I want to search for doctors by specialization so that I can find a suitable doctor.",
            "acceptance_criteria": [
                "Given the doctor directory is available, when the patient selects a specialization, matching doctors should be displayed."
            ]
        },
        {
            "story": "As a patient, I want to book an appointment so that I can consult a doctor.",
            "acceptance_criteria": [
                "Given an appointment slot is available, when the patient confirms booking, the appointment should be created.",
                "A booked slot should no longer be available to other users."
            ]
        }
    ],

    [
        {
            "requirement": "Patient registration",
            "priority": "Must Have",
            "reason": "Patients need accounts to manage appointments."
        },
        {
            "requirement": "Doctor search",
            "priority": "Must Have",
            "reason": "Patients need to locate appropriate doctors."
        },
        {
            "requirement": "Appointment booking",
            "priority": "Must Have",
            "reason": "Booking is the core workflow."
        },
        {
            "requirement": "Appointment reminders",
            "priority": "Should Have",
            "reason": "Reminders help users manage appointments."
        }
    ],

    [
        "Which doctor specializations should be supported?",
        "What information should patients provide during registration?",
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
            "expected": "The appointment should be created successfully."
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
# HOTEL DEMO
# =========================================================

hotel_data = make_demo(

    [
        "Users should be able to search hotels by location.",
        "Users should be able to view available rooms.",
        "Users should be able to compare room options.",
        "Users should be able to reserve rooms.",
        "Users should be able to make online payments.",
        "Users should receive booking confirmations."
    ],

    [
        "Payment and personal information should be protected.",
        "Room availability should be updated reliably.",
        "Search results should load quickly.",
        "The platform should support multiple bookings."
    ],

    [
        {
            "story": "As a traveler, I want to search hotels so that I can find accommodation.",
            "acceptance_criteria": [
                "Given a destination is entered, when the user searches, available hotels should be displayed."
            ]
        },
        {
            "story": "As a traveler, I want to reserve a room so that I can secure accommodation.",
            "acceptance_criteria": [
                "Given a room is available, when the user confirms the booking, the reservation should be created."
            ]
        }
    ],

    [
        {
            "requirement": "Hotel search",
            "priority": "Must Have",
            "reason": "Users need to discover hotels."
        },
        {
            "requirement": "Room availability",
            "priority": "Must Have",
            "reason": "Users need current room information."
        },
        {
            "requirement": "Room booking",
            "priority": "Must Have",
            "reason": "Booking is the primary platform workflow."
        },
        {
            "requirement": "Room comparison",
            "priority": "Should Have",
            "reason": "Comparison helps users choose rooms."
        }
    ],

    [
        "Which locations should be supported?",
        "What cancellation policy should apply?",
        "Which payment methods should be available?",
        "How should room availability be synchronized?"
    ],

    [
        {
            "id": "TC-01",
            "scenario": "User searches for hotels in a destination.",
            "expected": "Available hotels should be displayed."
        },
        {
            "id": "TC-02",
            "scenario": "User selects an available room.",
            "expected": "Room details and availability should be displayed."
        },
        {
            "id": "TC-03",
            "scenario": "User completes a room booking.",
            "expected": "A booking confirmation should be generated."
        },
        {
            "id": "TC-04",
            "scenario": "User attempts to book an unavailable room.",
            "expected": "The booking should not be confirmed."
        }
    ],

    [
        "Hotel database",
        "Room inventory service",
        "Booking backend",
        "Payment gateway",
        "Notification service",
        "Web frontend"
    ]
)


# =========================================================
# RIDE BOOKING DEMO
# =========================================================

ride_data = make_demo(

    [
        "Users should be able to enter pickup and drop locations.",
        "Users should be able to request a ride.",
        "Users should be able to view estimated fares.",
        "Users should be able to track the assigned driver.",
        "Users should be able to make digital payments.",
        "Users should be able to rate completed rides."
    ],

    [
        "Location data should be securely handled.",
        "Driver location should update reliably.",
        "Ride requests should be processed quickly.",
        "Payment information should be protected."
    ],

    [
        {
            "story": "As a rider, I want to enter pickup and drop locations so that I can request transportation.",
            "acceptance_criteria": [
                "Given valid locations are entered, when the user requests a ride, the system should process the request."
            ]
        },
        {
            "story": "As a rider, I want to track my driver so that I know when the ride will arrive.",
            "acceptance_criteria": [
                "Given a driver is assigned, the driver's current location should be displayed."
            ]
        }
    ],

    [
        {
            "requirement": "Ride request",
            "priority": "Must Have",
            "reason": "Requesting rides is the core functionality."
        },
        {
            "requirement": "Fare estimation",
            "priority": "Must Have",
            "reason": "Users need pricing information before confirmation."
        },
        {
            "requirement": "Driver tracking",
            "priority": "Must Have",
            "reason": "Tracking provides ride visibility."
        },
        {
            "requirement": "Ride rating",
            "priority": "Should Have",
            "reason": "Ratings provide feedback about completed rides."
        }
    ],

    [
        "How should fares be calculated?",
        "What vehicle types should be supported?",
        "How should driver assignment work?",
        "Which payment methods should be supported?"
    ],

    [
        {
            "id": "TC-01",
            "scenario": "User enters valid pickup and drop locations.",
            "expected": "The system should calculate and display an estimated fare."
        },
        {
            "id": "TC-02",
            "scenario": "User confirms a ride request.",
            "expected": "A driver should be assigned when available."
        },
        {
            "id": "TC-03",
            "scenario": "User tracks an active ride.",
            "expected": "Driver location should be displayed."
        },
        {
            "id": "TC-04",
            "scenario": "User completes payment.",
            "expected": "Payment should be recorded successfully."
        }
    ],

    [
        "Maps/location API",
        "Driver management backend",
        "Ride matching service",
        "Payment gateway",
        "Notification service",
        "Mobile frontend"
    ]
)


# =========================================================
# JOB PORTAL DEMO
# =========================================================

job_data = make_demo(

    [
        "Job seekers should be able to create profiles.",
        "Job seekers should be able to search and filter jobs.",
        "Job seekers should be able to upload resumes.",
        "Job seekers should be able to apply for jobs.",
        "Job seekers should be able to track application status.",
        "Employers should be able to post job vacancies and review applications."
    ],

    [
        "Candidate and employer data should be protected.",
        "Job searches should return results quickly.",
        "The platform should support multiple employers and candidates.",
        "Resume files should be securely stored."
    ],

    [
        {
            "story": "As a job seeker, I want to search jobs so that I can find suitable opportunities.",
            "acceptance_criteria": [
                "Given jobs are available, when the user applies filters, matching jobs should be displayed."
            ]
        },
        {
            "story": "As a job seeker, I want to apply for a job so that I can be considered for employment.",
            "acceptance_criteria": [
                "Given a valid resume exists, when the user submits an application, the application should be recorded."
            ]
        }
    ],

    [
        {
            "requirement": "Candidate profile",
            "priority": "Must Have",
            "reason": "Candidates need profiles for applications."
        },
        {
            "requirement": "Job search",
            "priority": "Must Have",
            "reason": "Searching is essential to finding opportunities."
        },
        {
            "requirement": "Job application",
            "priority": "Must Have",
            "reason": "Applications are the core workflow."
        },
        {
            "requirement": "Application tracking",
            "priority": "Should Have",
            "reason": "Tracking helps candidates monitor applications."
        }
    ],

    [
        "Which job categories should be supported?",
        "What resume file formats should be accepted?",
        "What information should employers provide?",
        "Should employers be able to reject applications directly?"
    ],

    [
        {
            "id": "TC-01",
            "scenario": "Candidate searches for a job.",
            "expected": "Matching jobs should be displayed."
        },
        {
            "id": "TC-02",
            "scenario": "Candidate uploads a valid resume.",
            "expected": "The resume should be stored successfully."
        },
        {
            "id": "TC-03",
            "scenario": "Candidate applies for a job.",
            "expected": "The application should be recorded."
        },
        {
            "id": "TC-04",
            "scenario": "Employer views applications.",
            "expected": "Submitted candidate applications should be displayed."
        }
    ],

    [
        "Candidate database",
        "Employer database",
        "Job listing service",
        "Resume storage",
        "Application management backend",
        "Authentication system"
    ]
)


# =========================================================
# ONLINE EXAM DEMO
# =========================================================

exam_data = make_demo(

    [
        "Students should be able to register for exams.",
        "Students should be able to view exam instructions.",
        "Students should be able to answer exam questions.",
        "Students should be able to submit exams.",
        "The system should calculate and display results.",
        "Administrators should be able to create exams and manage questions."
    ],

    [
        "Exam submissions should be securely stored.",
        "The platform should remain available during exams.",
        "The system should prevent unauthorized access.",
        "Results should be calculated accurately."
    ],

    [
        {
            "story": "As a student, I want to take an online exam so that I can complete my assessment remotely.",
            "acceptance_criteria": [
                "Given the student is registered, when the exam starts, the available questions should be displayed.",
                "The student's answers should be saved during the exam."
            ]
        },
        {
            "story": "As an administrator, I want to create exams so that students can complete assessments.",
            "acceptance_criteria": [
                "Given administrator access, when an exam is created with valid questions, it should become available to registered students."
            ]
        }
    ],

    [
        {
            "requirement": "Student registration",
            "priority": "Must Have",
            "reason": "Students need authenticated access."
        },
        {
            "requirement": "Exam management",
            "priority": "Must Have",
            "reason": "Administrators need to create assessments."
        },
        {
            "requirement": "Exam submission",
            "priority": "Must Have",
            "reason": "Submission is required to complete an exam."
        },
        {
            "requirement": "Automatic results",
            "priority": "Should Have",
            "reason": "Automatic results reduce manual evaluation effort."
        }
    ],

    [
        "What question types should be supported?",
        "Should students be allowed to revisit previous questions?",
        "What happens if the student loses internet connection?",
        "When should results become available?"
    ],

    [
        {
            "id": "TC-01",
            "scenario": "Student starts a registered exam.",
            "expected": "Exam instructions and questions should be displayed."
        },
        {
            "id": "TC-02",
            "scenario": "Student selects an answer.",
            "expected": "The answer should be saved."
        },
        {
            "id": "TC-03",
            "scenario": "Student submits the exam.",
            "expected": "The submission should be stored successfully."
        },
        {
            "id": "TC-04",
            "scenario": "Student views the result.",
            "expected": "The calculated result should be displayed accurately."
        }
    ],

    [
        "Student authentication",
        "Exam database",
        "Question management system",
        "Exam submission backend",
        "Result calculation engine",
        "Admin dashboard"
    ]
)


# =========================================================
# MAP DEMOS
# =========================================================

demo_data_map = {

    "QuickCart Grocery Platform": quickcart_data,
    "AI Fitness Platform": fitness_data,
    "EV Charging Platform": ev_data,
    "Student Learning Platform": student_data,
    "Hospital Appointment System": hospital_data,
    "Smart Hotel Booking Platform": hotel_data,
    "Ride Booking Platform": ride_data,
    "Job Portal": job_data,
    "Online Exam Platform": exam_data
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
            tests[i].get(
                "id",
                f"TC-{i + 1:02d}"
            )
            if i < len(tests)
            else "-"
        )

        rows.append({

            "Requirement": requirement_id,

            "Requirement Description":
                requirement,

            "User Story": story_id,

            "User Story Description":
                story,

            "Test Case":
                test_id
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

    report.append(
        "REQPILOT - AI REQUIREMENTS ENGINEERING REPORT"
    )

    report.append("=" * 60)

    report.append("")

    report.append(
        "FUNCTIONAL REQUIREMENTS"
    )

    report.append("-" * 30)

    for i, req in enumerate(
        data.get(
            "functional_requirements",
            []
        ),
        1
    ):

        report.append(
            f"FR-{i:02d}: {req}"
        )

    report.append("")

    report.append(
        "NON-FUNCTIONAL REQUIREMENTS"
    )

    report.append("-" * 30)

    for i, req in enumerate(
        data.get(
            "non_functional_requirements",
            []
        ),
        1
    ):

        report.append(
            f"NFR-{i:02d}: {req}"
        )

    report.append("")

    report.append(
        "USER STORIES"
    )

    report.append("-" * 30)

    for i, story in enumerate(
        data.get(
            "user_stories",
            []
        ),
        1
    ):

        report.append(
            f"US-{i:02d}: "
            f"{story.get('story', '')}"
        )

        for criterion in story.get(
            "acceptance_criteria",
            []
        ):

            report.append(
                f"  - {criterion}"
            )

    report.append("")

    report.append(
        "PRIORITIES"
    )

    report.append("-" * 30)

    for item in data.get(
        "priorities",
        []
    ):

        report.append(
            f"{item.get('requirement', '')} "
            f"→ {item.get('priority', '')}"
        )

        report.append(
            f"Reason: "
            f"{item.get('reason', '')}"
        )

    report.append("")

    report.append(
        "AMBIGUITIES / GAPS"
    )

    report.append("-" * 30)

    for item in data.get(
        "ambiguities",
        []
    ):

        report.append(
            f"- {item}"
        )

    report.append("")

    report.append(
        "TEST CASES"
    )

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
            f"Expected: "
            f"{test.get('expected', '')}"
        )

    report.append("")

    report.append(
        "TECHNICAL DEPENDENCIES"
    )

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

    st.subheader(
        "📊 Generated Requirements"
    )

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

            with st.container(border=True):

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

            with st.container(border=True):

                st.write(
                    f"**NFR-{i:02d}**"
                )

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
                    f"Priority: "
                    f"**{item.get('priority', 'N/A')}**"
                )

                st.caption(
                    item.get(
                        "reason",
                        ""
                    )
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
# LIVE GEMINI ANALYSIS
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

    if preset in demo_data_map:

        st.success(
            f"🎬 Demo Mode activated — {preset}"
        )

        st.caption(
            "Pre-generated demo data is being displayed. "
            "No Gemini API call is required."
        )

        display_results(
            demo_data_map[preset]
        )

    else:

        st.info(
            "🎬 Select any demo preset from the sidebar "
            "and click Demo Mode."
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
        "We contribute through structured multi-stage requirement analysis, "
        "including requirement classification, ambiguity detection, "
        "prioritization, user-story generation, test-case generation, "
        "summary analysis, and requirement traceability from a single "
        "project description."
    )


# =========================================================
# FOOTER
# =========================================================

st.write("")

st.caption(
    "ReqPilot • G14 • AI Requirements Engineering Agent"
)
