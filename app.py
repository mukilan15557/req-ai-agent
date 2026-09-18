import streamlit as st
from google import genai

st.set_page_config(
    page_title="FoundersPRD | AI Startup Requirements Agent",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 FoundersPRD: Autonomous Startup Requirements Agent")
st.caption("Convert raw startup ideas into Lean MVPs, MoSCoW Specs, and Agile User Stories.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Agent Settings")
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        api_key = st.text_input("Enter Gemini API Key:", type="password")
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

sample_pitches = {
    "AI Cold Outreach Tool for Freelancers": "We want an AI platform where freelance developers upload their portfolio and it automatically finds startup founders on LinkedIn, writes hyper-personalized pitch emails, tracks responses, and suggests meeting times via Calendly.",
    "Peer-to-Peer EV Charging Network": "Airbnb for electric car chargers. Homeowners with home wall chargers rent out their driveway plug to EV drivers who need an emergency charge. Needs dynamic electricity rate pricing and automatic payouts.",
    "Micro-SaaS Churn Predictor": "A lightweight widget for Shopify store owners that detects when a customer is about to cancel a recurring order, offers a dynamic discount or pause option, and provides an analytics dashboard on churn reasons."
}

default_input = sample_pitches.get(preset, "")

# Main Input Section
startup_pitch = st.text_area(
    "Enter Startup Pitch, Problem Statement, or Raw Notes:",
    value=default_input,
    height=160,
    placeholder="Describe the problem, target audience, and how the product solves it..."
)

col_run, _ = st.columns([1, 4])
with col_run:
    generate_btn = st.button("⚡ Generate PRD & Roadmap", type="primary")

# Generation Logic
if generate_btn:
    if not api_key:
        st.error("Please provide your Gemini API key in the sidebar or via Streamlit Secrets.")
    elif not startup_pitch.strip():
        st.warning("Please enter a startup pitch or select a preset.")
    else:
        client = genai.Client(api_key=api_key)

        prompt = f"""
You are an elite Chief Product Officer (CPO) and Agile Requirements Engineering Agent.
Analyze the following startup concept and produce a comprehensive, publication-grade Product Requirements Document (PRD).

Startup Pitch:
\"\"\"{startup_pitch}\"\"\"

Structure your output strictly using these 4 Markdown sections:

### 1. Target Persona & Value Proposition
- **Ideal Customer Profile (ICP)**: Who will be the first 100 paying customers?
- **Core Pain Point**: The exact friction or waste being addressed.
- **Unfair Advantage**: Why this solution beats manual alternatives.

### 2. MVP Scope (MoSCoW Framework)
- **Must Have (Day 1 Launch)**: The bare essential features required to validate the hypothesis.
- **Should Have (Next Sprint)**: Key secondary features once user retention is validated.
- **Won't Have (Scope Creep Guardrail)**: Features the team MUST NOT build right now to prevent burning runway.

### 3. Engineering User Stories & BDD Scenarios
Provide 2 high-priority Agile user stories:
- Format: **As a** [Persona], **I want to** [Action], **So that** [Outcome].
- Include executable **Gherkin Acceptance Criteria (Given / When / Then)** for both the happy path and a failure edge case.

### 4. Technical Feasibility & Blind Spot Audit
- **Architecture Dependencies**: Essential third-party APIs, authentication protocols, and databases.
- **Critical Risk / Blind Spot**: What single operational, security, or economic factor could break this product early on?
"""

        with st.spinner("Analyzing market fit, scoping MVP, and generating technical specs..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                
                st.success("PRD Specification Generated Successfully!")
                st.markdown("---")
                st.markdown(response.text)
                
                st.download_button(
                    label="📥 Download Specification (.md)",
                    data=response.text,
                    file_name="Startup_PRD_Specification.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"Execution Error: {e}")
