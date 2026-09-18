import streamlit as st
import time
from google import genai

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="FoundersPRD | AI Startup Requirements Agent",
    page_icon="🚀",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🚀 FoundersPRD: Autonomous Startup Requirements Agent")

st.caption(
    "Convert raw startup ideas into Lean MVPs, MoSCoW Specs, and Agile User Stories."
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.header("⚙️ Agent Settings")

    api_key = st.secrets.get("GEMINI_API_KEY", "")

    if not api_key:
        api_key = st.text_input(
            "Enter Gemini API Key:",
            type="password"
        )
    else:
        st.success("API Key Loaded from Secrets")

    st.markdown("---")

    st.subheader("💡 Demo Pitch Presets")

    preset = st.selectbox(
        "Choose an example startup idea:",
        [
            "Custom Idea",
            "AI Cold Outreach Tool for Freelancers",
            "Peer-to-Peer EV Charging Network",
            "Micro-SaaS Churn Predictor"
        ]
    )

# --------------------------------------------------
# SAMPLE PITCHES
# --------------------------------------------------

sample_pitches = {
    "AI Cold Outreach Tool for Freelancers":
        "We want an AI platform where freelance developers upload their portfolio "
        "and it automatically finds startup founders on LinkedIn, writes "
        "hyper-personalized pitch emails, tracks responses, and suggests meeting "
        "times via Calendly.",

    "Peer-to-Peer EV Charging Network":
        "Airbnb for electric car chargers. Homeowners with home wall chargers "
        "rent out their driveway plug to EV drivers who need an emergency charge. "
        "Needs dynamic electricity rate pricing and automatic payouts.",

    "Micro-SaaS Churn Predictor":
        "A lightweight widget for Shopify store owners that detects when a "
        "customer is about to cancel a recurring order, offers a dynamic "
        "discount or pause option, and provides an analytics dashboard on "
        "churn reasons."
}

default_input = sample_pitches.get(preset, "")

# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

startup_pitch = st.text_area(
    "Enter Startup Pitch, Problem Statement, or Raw Notes:",
    value=default_input,
    height=160,
    placeholder=(
        "Describe the problem, target audience, "
        "and how the product solves it..."
    )
)

# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

col_run, _ = st.columns([1, 4])

with col_run:
    generate_btn = st.button(
        "⚡ Generate PRD & Roadmap",
        type="primary"
    )

# --------------------------------------------------
# AI GENERATION
# --------------------------------------------------

if generate_btn:

    # Check API key
    if not api_key:
        st.error(
            "Please provide your Gemini API key in the sidebar "
            "or via Streamlit Secrets."
        )

    # Check user input
    elif not startup_pitch.strip():
        st.warning(
            "Please enter a startup pitch or select a preset."
        )

    else:

        # Create Gemini client
        client = genai.Client(api_key=api_key)

        # --------------------------------------------------
        # PROMPT
        # --------------------------------------------------

        prompt = f"""
You are an elite Chief Product Officer (CPO) and Agile Requirements
Engineering Agent.

Analyze the following startup concept and produce a comprehensive,
publication-grade Product Requirements Document (PRD).

Startup Pitch:
\"\"\"{startup_pitch}\"\"\"

Structure your output strictly using these 4 Markdown sections:

### 1. Target Persona & Value Proposition

- **Ideal Customer Profile (ICP)**:
  Who will be the first 100 paying customers?

- **Core Pain Point**:
  The exact friction or waste being addressed.

- **Unfair Advantage**:
  Why this solution beats manual alternatives.

### 2. MVP Scope (MoSCoW Framework)

- **Must Have (Day 1 Launch)**:
  The bare essential features required to validate the hypothesis.

- **Should Have (Next Sprint)**:
  Key secondary features once user retention is validated.

- **Won't Have (Scope Creep Guardrail)**:
  Features the team MUST NOT build right now to prevent scope creep.

### 3. Engineering User Stories & BDD Scenarios

Provide 2 high-priority Agile user stories.

Format:

**As a** [Persona],
**I want to** [Action],
**So that** [Outcome].

Include executable Gherkin Acceptance Criteria
(Given / When / Then) for both:

1. Happy path
2. Failure edge case

### 4. Technical Feasibility & Blind Spot Audit

- **Architecture Dependencies**:
  Essential third-party APIs, authentication protocols,
  databases, and external services.

- **Critical Risk / Blind Spot**:
  What single operational, security, technical, or economic
  factor could break this product early?

Keep the response structured, practical, and suitable for
a software engineering team.
"""

        # --------------------------------------------------
        # GEMINI REQUEST WITH RETRY
        # --------------------------------------------------

        with st.spinner(
            "🤖 Analyzing market fit, scoping MVP, and generating technical specs..."
        ):

            response = None

            for attempt in range(3):

                try:

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )

                    # Success
                    break

                except Exception as e:

                    error_message = str(e)

                    # Handle temporary 503 error
                    if "503" in error_message:

                        if attempt < 2:

                            wait_time = 2 ** attempt

                            st.warning(
                                f"⚠️ Gemini is temporarily busy. "
                                f"Retrying in {wait_time} seconds..."
                            )

                            time.sleep(wait_time)

                        else:

                            st.error(
                                "❌ Gemini is currently unavailable "
                                "after multiple attempts."
                            )

                            st.info(
                                "Please try again after a short wait."
                            )

                    else:

                        st.error(
                            f"❌ Execution Error: {e}"
                        )

                        break

            # --------------------------------------------------
            # DISPLAY RESULT
            # --------------------------------------------------

            if response is not None:

                st.success(
                    "✅ PRD Specification Generated Successfully!"
                )

                st.markdown("---")

                st.markdown(response.text)

                # --------------------------------------------------
                # DOWNLOAD
                # --------------------------------------------------

                st.download_button(
                    label="📥 Download Specification (.md)",
                    data=response.text,
                    file_name="Startup_PRD_Specification.md",
                    mime="text/markdown"
                )
