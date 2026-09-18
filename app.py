import streamlit as st
import json
import time
from google import genai
from google.genai import types


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="QuickCart + ReqPilot",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "order_placed" not in st.session_state:
    st.session_state.order_placed = False


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top left, #172554 0%, transparent 35%),
        radial-gradient(circle at bottom right, #064e3b 0%, transparent 35%),
        #020617;
    color: white;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 10px;
}

h1, h2, h3 {
    color: white;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}

.stTextInput input,
.stTextArea textarea {
    border-radius: 10px;
}

.metric-card {
    padding: 18px;
    border-radius: 15px;
    background: rgba(255,255,255,0.06);
    text-align: center;
}

.product-card {
    padding: 18px;
    border-radius: 16px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 10px;
}

.login-box {
    max-width: 450px;
    margin: auto;
}

.small-muted {
    color: #94a3b8;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        with st.container(border=True):

            st.markdown(
                "<div style='text-align:center'>"
                "<h1>🛒 QuickCart</h1>"
                "<p>Welcome Back!</p>"
                "</div>",
                unsafe_allow_html=True
            )

            username = st.text_input(
                "Username",
                placeholder="Enter username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button(
                "🔐 Login",
                type="primary",
                use_container_width=True
            ):

                if username == "admin" and password == "quickcart123":

                    st.session_state.logged_in = True
                    st.success("Login successful!")
                    time.sleep(0.5)
                    st.rerun()

                else:
                    st.error("Invalid username or password.")

            st.caption("Demo Account")
            st.code("Username: admin\nPassword: quickcart123")

            st.markdown(
                "<p class='small-muted' style='text-align:center'>"
                "Demo authentication for hackathon presentation"
                "</p>",
                unsafe_allow_html=True
            )


# =========================================================
# QUICKCART PRODUCTS
# =========================================================

products = {
    "Milk": {
        "price": 45,
        "category": "Dairy",
        "emoji": "🥛"
    },
    "Bread": {
        "price": 40,
        "category": "Bakery",
        "emoji": "🍞"
    },
    "Rice 5kg": {
        "price": 320,
        "category": "Staples",
        "emoji": "🍚"
    },
    "Eggs (12)": {
        "price": 75,
        "category": "Dairy",
        "emoji": "🥚"
    },
    "Apples 1kg": {
        "price": 140,
        "category": "Fruits",
        "emoji": "🍎"
    },
    "Bananas": {
        "price": 60,
        "category": "Fruits",
        "emoji": "🍌"
    },
    "Tomatoes 1kg": {
        "price": 55,
        "category": "Vegetables",
        "emoji": "🍅"
    },
    "Potatoes 1kg": {
        "price": 50,
        "category": "Vegetables",
        "emoji": "🥔"
    }
}


# =========================================================
# GROCERY STORE
# =========================================================

def grocery_store():

    st.title("🛒 QuickCart")
    st.caption("Fast & simple grocery delivery platform")

    # -----------------------------------------------------
    # TOP BAR
    # -----------------------------------------------------

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.subheader("Welcome, Admin 👋")

    with col2:
        st.metric(
            "Cart Items",
            sum(st.session_state.cart.values())
        )

    with col3:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.cart = {}
            st.rerun()

    st.divider()

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    search = st.text_input(
        "🔎 Search groceries",
        placeholder="Search milk, rice, apples..."
    )

    filtered_products = {
        name: info
        for name, info in products.items()
        if search.lower() in name.lower()
    }

    st.subheader("🛍️ Available Groceries")

    # -----------------------------------------------------
    # PRODUCT CARDS
    # -----------------------------------------------------

    product_list = list(filtered_products.items())

    if not product_list:
        st.warning("No products found.")

    else:

        for i in range(0, len(product_list), 4):

            cols = st.columns(4)

            for col, (name, info) in zip(
                cols,
                product_list[i:i + 4]
            ):

                with col:

                    with st.container(border=True):

                        st.markdown(
                            f"<div style='text-align:center;"
                            f"font-size:45px'>{info['emoji']}</div>",
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"### {name}"
                        )

                        st.caption(info["category"])

                        st.write(
                            f"**₹{info['price']}**"
                        )

                        if st.button(
                            "➕ Add to Cart",
                            key=f"add_{name}",
                            use_container_width=True
                        ):

                            if name not in st.session_state.cart:
                                st.session_state.cart[name] = 0

                            st.session_state.cart[name] += 1

                            st.toast(
                                f"{name} added to cart!"
                            )

    st.divider()

    # -----------------------------------------------------
    # CART
    # -----------------------------------------------------

    st.subheader("🛍️ Your Cart")

    if not st.session_state.cart:

        st.info("Your cart is empty.")

    else:

        total = 0

        for name, quantity in list(
            st.session_state.cart.items()
        ):

            price = products[name]["price"]
            subtotal = price * quantity
            total += subtotal

            col1, col2, col3, col4 = st.columns(
                [3, 1, 1, 1]
            )

            with col1:
                st.write(
                    f"{products[name]['emoji']} **{name}**"
                )

            with col2:
                st.write(f"₹{price}")

            with col3:

                new_quantity = st.number_input(
                    "Qty",
                    min_value=0,
                    value=quantity,
                    step=1,
                    key=f"qty_{name}"
                )

                if new_quantity == 0:
                    del st.session_state.cart[name]
                    st.rerun()

                elif new_quantity != quantity:
                    st.session_state.cart[name] = new_quantity
                    st.rerun()

            with col4:
                st.write(f"₹{subtotal}")

        st.divider()

        st.markdown(
            f"## Total: ₹{total}"
        )

        if st.button(
            "💳 Proceed to Checkout",
            type="primary",
            use_container_width=True
        ):

            st.session_state.order_placed = True
            st.success(
                "🎉 Demo order placed successfully!"
            )

            st.balloons()

            st.session_state.cart = {}


# =========================================================
# GEMINI PROMPT
# =========================================================

def create_prompt(idea):

    return f"""
You are an AI Requirements Engineering Agent.

Analyze the following software/project idea:

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

1. Separate Functional Requirements and Non-Functional Requirements.
2. Write clear Agile user stories.
3. Use Given-When-Then style acceptance criteria.
4. Use MoSCoW priorities:
   Must Have, Should Have, Could Have, Won't Have.
5. Detect missing, unclear or ambiguous requirements.
6. Generate realistic test cases.
7. Identify technical dependencies.
8. Keep everything concise.
9. Do not invent unnecessary features.
10. Return valid JSON only.
"""


# =========================================================
# GEMINI ANALYSIS
# =========================================================

def analyze_with_gemini(idea, key):

    prompt = create_prompt(idea)

    client = genai.Client(api_key=key)

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
                "503" in error_text
                or "UNAVAILABLE" in error_text
            ):

                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue

            raise e


# =========================================================
# DEMO DATA
# =========================================================

quickcart_data = {

    "functional_requirements": [
        "Users can create an account and log in.",
        "Users can browse and search grocery products.",
        "Users can add products to a shopping cart.",
        "Users can place orders and make online payments.",
        "Users can track their orders.",
        "Users receive order status notifications."
    ],

    "non_functional_requirements": [
        "Personal and payment data must be securely handled.",
        "Product search should respond quickly.",
        "The platform should remain available during normal usage.",
        "The system should support multiple concurrent users."
    ],

    "user_stories": [

        {
            "story": "As a customer, I want to search for groceries so that I can quickly find products.",
            "acceptance_criteria": [
                "Given the user is on the product page",
                "When the user searches for a product",
                "Then matching products should be displayed."
            ]
        },

        {
            "story": "As a customer, I want to place an order so that groceries can be delivered to me.",
            "acceptance_criteria": [
                "Given the cart contains products",
                "When the user completes checkout",
                "Then an order should be created."
            ]
        },

        {
            "story": "As a customer, I want to track my order so that I know its delivery status.",
            "acceptance_criteria": [
                "Given an order has been placed",
                "When the customer opens order tracking",
                "Then the current order status should be displayed."
            ]
        }

    ],

    "priorities": [

        {
            "requirement": "User login",
            "priority": "Must Have",
            "reason": "Required to identify customers."
        },

        {
            "requirement": "Product search",
            "priority": "Must Have",
            "reason": "Core grocery shopping functionality."
        },

        {
            "requirement": "Shopping cart",
            "priority": "Must Have",
            "reason": "Required to create an order."
        },

        {
            "requirement": "Online payment",
            "priority": "Must Have",
            "reason": "Required for online checkout."
        },

        {
            "requirement": "Order tracking",
            "priority": "Should Have",
            "reason": "Improves customer visibility."
        },

        {
            "requirement": "Personalized recommendations",
            "priority": "Could Have",
            "reason": "Useful but not essential for the core system."
        }

    ],

    "ambiguities": [
        "Which payment methods are supported?",
        "Which delivery areas are supported?",
        "What happens when a product becomes out of stock after being added to the cart?",
        "Can customers cancel orders?",
        "What is the expected delivery time?",
        "Which notification channels are supported?"
    ],

    "test_cases": [

        {
            "id": "TC-01",
            "scenario": "Search for a grocery product",
            "expected": "Matching products are displayed."
        },

        {
            "id": "TC-02",
            "scenario": "Change cart quantity",
            "expected": "Cart quantity and total price are updated."
        },

        {
            "id": "TC-03",
            "scenario": "Successful payment",
            "expected": "Order is created successfully."
        },

        {
            "id": "TC-04",
            "scenario": "Failed payment",
            "expected": "Order is not confirmed and an error is shown."
        },

        {
            "id": "TC-05",
            "scenario": "Track an existing order",
            "expected": "Current delivery status is displayed."
        }

    ],

    "technical_dependencies": [
        "Authentication system",
        "Product and inventory database",
        "Order management backend",
        "Payment gateway",
        "Delivery tracking service",
        "Notification service",
        "Frontend application"
    ]
}


# =========================================================
# DISPLAY AI RESULTS
# =========================================================

def display_results(data):

    st.divider()

    st.header("🤖 Generated Requirements")

    tabs = st.tabs([
        "📋 Requirements",
        "👤 User Stories",
        "🎯 Priorities",
        "⚠️ Ambiguities",
        "🧪 Test Cases",
        "🔗 Dependencies"
    ])

    # -----------------------------------------------------
    # REQUIREMENTS
    # -----------------------------------------------------

    with tabs[0]:

        st.subheader("Functional Requirements")

        for i, item in enumerate(
            data.get("functional_requirements", []),
            1
        ):
            st.write(f"**FR-{i}:** {item}")

        st.subheader("Non-Functional Requirements")

        for i, item in enumerate(
            data.get("non_functional_requirements", []),
            1
        ):
            st.write(f"**NFR-{i}:** {item}")

    # -----------------------------------------------------
    # USER STORIES
    # -----------------------------------------------------

    with tabs[1]:

        for i, story in enumerate(
            data.get("user_stories", []),
            1
        ):

            with st.container(border=True):

                st.markdown(
                    f"### User Story {i}"
                )

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
                    st.write(f"• {criterion}")

    # -----------------------------------------------------
    # PRIORITIES
    # -----------------------------------------------------

    with tabs[2]:

        for item in data.get(
            "priorities",
            []
        ):

            st.write(
                f"**{item.get('priority', '')}** — "
                f"{item.get('requirement', '')}"
            )

            st.caption(
                item.get("reason", "")
            )

    # -----------------------------------------------------
    # AMBIGUITIES
    # -----------------------------------------------------

    with tabs[3]:

        for item in data.get(
            "ambiguities",
            []
        ):
            st.warning(item)

    # -----------------------------------------------------
    # TEST CASES
    # -----------------------------------------------------

    with tabs[4]:

        for test in data.get(
            "test_cases",
            []
        ):

            with st.container(border=True):

                st.markdown(
                    f"### {test.get('id', '')}"
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
    # DEPENDENCIES
    # -----------------------------------------------------

    with tabs[5]:

        for dependency in data.get(
            "technical_dependencies",
            []
        ):
            st.write(f"🔗 {dependency}")

    # -----------------------------------------------------
    # DOWNLOAD
    # -----------------------------------------------------

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
# REQPILOT PAGE
# =========================================================

def reqpilot_page():

    st.title("🚀 ReqPilot")

    st.caption(
        "AI Requirements Engineering Agent • Problem Statement G14"
    )

    st.markdown(
        """
        Turn an informal project idea into structured
        software requirements, user stories, priorities,
        ambiguity detection and test cases.
        """
    )

    # -----------------------------------------------------
    # API KEY
    # -----------------------------------------------------

    api_key = None

    try:
        api_key = st.secrets["GEMINI_API_KEY"]

        if api_key:
            st.success("🔑 Gemini API connected")

    except Exception:

        api_key = st.text_input(
            "Gemini API Key",
            type="password"
        )

    # -----------------------------------------------------
    # SCENARIO
    # -----------------------------------------------------

    scenario = st.selectbox(
        "🎬 Demo Scenario",
        [
            "Custom Idea",
            "🛒 QuickCart — Grocery Delivery",
            "⚡ EVCharge — EV Charging Platform"
        ]
    )

    # -----------------------------------------------------
    # IDEA
    # -----------------------------------------------------

    if scenario == "🛒 QuickCart — Grocery Delivery":

        default_idea = """
        I want to build a grocery delivery platform called QuickCart.

        Users should be able to create an account, browse and search
        groceries, add products to a cart, make payments, place orders,
        track deliveries and receive notifications.
        """

    elif scenario == "⚡ EVCharge — EV Charging Platform":

        default_idea = """
        I want to build an EV charging platform called EVCharge.

        The platform should help EV users find nearby charging stations,
        check real-time availability, reserve a charging slot,
        make payments and receive notifications.

        Charging station operators should be able to manage station
        and slot availability.
        """

    else:

        default_idea = ""

    idea = st.text_area(
        "💡 Describe your project idea",
        value=default_idea,
        height=180,
        placeholder="Example: I want to build an online grocery delivery app..."
    )

    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    words = len(idea.split())

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Input Words", words)

    with col2:
        st.metric("AI Modules", "6")

    with col3:
        st.metric("Artifacts", "6")

    with col4:
        st.metric("AI Engine", "Gemini")

    # -----------------------------------------------------
    # PIPELINE
    # -----------------------------------------------------

    st.subheader("⚙️ Requirements Pipeline")

    pipeline = [
        ("Raw Idea", "User Input"),
        ("Extract", "Requirements"),
        ("Classify", "FR / NFR"),
        ("Prioritize", "MoSCoW"),
        ("Detect Gaps", "Ambiguities"),
        ("Test Cases", "Validation")
    ]

    cols = st.columns(6)

    for col, (title, subtitle) in zip(
        cols,
        pipeline
    ):

        with col:

            with st.container(border=True):

                st.markdown(
                    f"**{title}**"
                )

                st.caption(subtitle)

    st.divider()

    # -----------------------------------------------------
    # ACTION BUTTONS
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # LIVE GEMINI
    # -----------------------------------------------------

    if analyze:

        if not idea.strip():

            st.warning(
                "Please enter a project idea."
            )

        elif not api_key:

            st.error(
                "Gemini API key is required."
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
                        "Requirements generated successfully!"
                    )

                    display_results(result)

                except Exception as e:

                    st.error(
                        f"AI analysis failed: {e}"
                    )

    # -----------------------------------------------------
    # DEMO MODE
    # -----------------------------------------------------

    if demo:

        if scenario == "🛒 QuickCart — Grocery Delivery":

            st.success(
                "🎬 QuickCart Demo Mode activated"
            )

            display_results(
                quickcart_data
            )

        elif scenario == "⚡ EVCharge — EV Charging Platform":

            st.info(
                "EVCharge demo data can be connected here."
            )

        else:

            st.info(
                "Please select QuickCart or EVCharge "
                "from the Demo Scenario dropdown."
            )


# =========================================================
# MAIN APP
# =========================================================

if not st.session_state.logged_in:

    login_page()

else:

    # -----------------------------------------------------
    # SIDEBAR
    # -----------------------------------------------------

    with st.sidebar:

        st.title("🛒 QuickCart")

        st.caption(
            "Grocery Delivery Demo"
        )

        st.divider()

        st.subheader("Navigation")

        page = st.radio(
            "Go to",
            [
                "🛒 Grocery Store",
                "🚀 ReqPilot"
            ]
        )

        st.divider()

        st.caption(
            "Logged in as: admin"
        )

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.cart = {}
            st.rerun()

    # -----------------------------------------------------
    # PAGE ROUTING
    # -----------------------------------------------------

    if page == "🛒 Grocery Store":

        grocery_store()

    else:

        reqpilot_page()
