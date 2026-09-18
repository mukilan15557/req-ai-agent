import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Liquid Glass AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# LIQUID GLASS CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --glass-white: rgba(255, 255, 255, 0.14);
    --glass-white-light: rgba(255, 255, 255, 0.20);
    --glass-border: rgba(255, 255, 255, 0.25);
    --text-primary: rgba(255,255,255,0.96);
    --text-secondary: rgba(255,255,255,0.62);
}

/* ==========================================================
   GLOBAL
   ========================================================== */

html, body, [class*="css"] {
    font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    min-height: 100vh;

    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(90, 210, 255, 0.50),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(70, 140, 255, 0.42),
            transparent 30%
        ),
        radial-gradient(
            circle at 50% 90%,
            rgba(0, 190, 255, 0.30),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #03141e 0%,
            #062a3d 45%,
            #041b2b 100%
        );

    background-attachment: fixed;
}

/* ==========================================================
   REMOVE STREAMLIT DEFAULTS
   ========================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

.block-container {
    max-width: 1450px;
    padding-top: 35px;
    padding-bottom: 60px;
}

/* ==========================================================
   LIQUID GLASS MAIN CONTAINER
   ========================================================== */

.liquid-glass {

    position: relative;

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.19),
            rgba(255,255,255,0.07)
        );

    border: 1px solid rgba(255,255,255,0.25);

    border-radius: 32px;

    backdrop-filter: blur(35px) saturate(160%);
    -webkit-backdrop-filter: blur(35px) saturate(160%);

    box-shadow:

        inset 0 1px 1px rgba(255,255,255,0.40),

        inset 0 -1px 1px rgba(0,0,0,0.15),

        inset 1px 0 rgba(255,255,255,0.15),

        0 25px 70px rgba(0,0,0,0.28);
}

/* top glossy reflection */

.liquid-glass::before {

    content: "";

    position: absolute;

    left: 3%;
    right: 3%;
    top: 1px;

    height: 35%;

    border-radius: 32px 32px 50% 50%;

    background:
        linear-gradient(
            180deg,
            rgba(255,255,255,0.20),
            rgba(255,255,255,0)
        );

    pointer-events: none;
}

/* ==========================================================
   HERO
   ========================================================== */

.hero {

    position: relative;

    padding: 42px;

    margin-bottom: 25px;

    overflow: hidden;

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.20),
            rgba(255,255,255,0.06)
        );

    border: 1px solid rgba(255,255,255,0.27);

    border-radius: 34px;

    backdrop-filter: blur(40px) saturate(170%);
    -webkit-backdrop-filter: blur(40px) saturate(170%);

    box-shadow:
        inset 0 1px 2px rgba(255,255,255,0.45),
        inset 0 -2px 5px rgba(0,0,0,0.10),
        0 30px 80px rgba(0,0,0,0.30);
}

/* ==========================================================
   HERO LIGHT
   ========================================================== */

.hero-light {

    position: absolute;

    width: 280px;
    height: 280px;

    right: -80px;
    top: -120px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(120,225,255,0.35),
            transparent 70%
        );

    filter: blur(20px);

    pointer-events: none;
}

/* ==========================================================
   TYPOGRAPHY
   ========================================================== */

.hero-title {

    position: relative;

    font-size: 44px;
    font-weight: 700;

    letter-spacing: -1.8px;

    color: var(--text-primary);

    margin-bottom: 8px;

    text-shadow:
        0 2px 20px rgba(0,0,0,0.20);
}

.hero-subtitle {

    position: relative;

    font-size: 16px;

    color: var(--text-secondary);

    max-width: 700px;

    line-height: 1.7;
}

.section-title {

    font-size: 20px;

    font-weight: 600;

    color: rgba(255,255,255,0.94);

    margin: 25px 0 14px 5px;

    letter-spacing: -0.3px;
}

/* ==========================================================
   GLASS CARDS
   ========================================================== */

.glass-card {

    position: relative;

    min-height: 145px;

    padding: 25px;

    overflow: hidden;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.18),
            rgba(255,255,255,0.055)
        );

    border: 1px solid rgba(255,255,255,0.22);

    border-radius: 25px;

    backdrop-filter: blur(30px) saturate(160%);
    -webkit-backdrop-filter: blur(30px) saturate(160%);

    box-shadow:
        inset 0 1px 1px rgba(255,255,255,0.30),
        inset 0 -1px 1px rgba(0,0,0,0.12),
        0 15px 40px rgba(0,0,0,0.20);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease,
        border 0.25s ease;
}

.glass-card:hover {

    transform: translateY(-4px);

    border: 1px solid rgba(255,255,255,0.36);

    box-shadow:
        inset 0 1px 1px rgba(255,255,255,0.40),
        0 22px 55px rgba(0,0,0,0.28);
}

/* card shine */

.glass-card::before {

    content: "";

    position: absolute;

    left: -20%;
    top: -80%;

    width: 140%;
    height: 150%;

    background:
        linear-gradient(
            120deg,
            transparent 35%,
            rgba(255,255,255,0.08) 50%,
            transparent 65%
        );

    transform: rotate(10deg);

    pointer-events: none;
}

/* ==========================================================
   ICON
   ========================================================== */

.glass-icon {

    width: 46px;
    height: 46px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 15px;

    margin-bottom: 15px;

    font-size: 20px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.25),
            rgba(255,255,255,0.08)
        );

    border: 1px solid rgba(255,255,255,0.25);

    box-shadow:
        inset 0 1px rgba(255,255,255,0.35),
        0 8px 20px rgba(0,0,0,0.16);
}

.card-title {

    font-size: 17px;

    font-weight: 600;

    color: rgba(255,255,255,0.95);

    margin-bottom: 7px;
}

.card-text {

    font-size: 13px;

    line-height: 1.6;

    color: rgba(255,255,255,0.58);
}

/* ==========================================================
   INPUT GLASS
   ========================================================== */

.stTextInput > div > div,
.stTextArea > div > div {

    background:
        rgba(255,255,255,0.075) !important;

    border:
        1px solid rgba(255,255,255,0.18) !important;

    border-radius:
        17px !important;

    backdrop-filter:
        blur(25px) saturate(150%) !important;

    -webkit-backdrop-filter:
        blur(25px) saturate(150%) !important;

    box-shadow:
        inset 0 1px rgba(255,255,255,0.12),
        inset 0 -1px rgba(0,0,0,0.10) !important;
}

.stTextInput input,
.stTextArea textarea {

    color: white !important;

    font-size: 14px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {

    color:
        rgba(255,255,255,0.40) !important;
}

/* ==========================================================
   SELECTBOX
   ========================================================== */

.stSelectbox > div > div {

    background:
        rgba(255,255,255,0.075) !important;

    border:
        1px solid rgba(255,255,255,0.18) !important;

    border-radius:
        17px !important;
}

/* ==========================================================
   BUTTON
   ========================================================== */

.stButton > button {

    width: 100%;

    height: 48px;

    border-radius: 17px;

    border: 1px solid rgba(255,255,255,0.30);

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.22),
            rgba(255,255,255,0.09)
        );

    color: white;

    font-size: 14px;

    font-weight: 600;

    backdrop-filter:
        blur(25px) saturate(170%);

    -webkit-backdrop-filter:
        blur(25px) saturate(170%);

    box-shadow:

        inset 0 1px 1px rgba(255,255,255,0.35),

        0 10px 30px rgba(0,0,0,0.18);

    transition:
        all 0.25s ease;
}

.stButton > button:hover {

    transform: translateY(-2px);

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.30),
            rgba(255,255,255,0.12)
        );

    border-color:
        rgba(255,255,255,0.45);

    box-shadow:

        inset 0 1px 1px rgba(255,255,255,0.45),

        0 15px 35px rgba(0,0,0,0.25);
}

/* ==========================================================
   METRIC GLASS
   ========================================================== */

[data-testid="stMetric"] {

    padding: 22px;

    border-radius: 22px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.15),
            rgba(255,255,255,0.055)
        );

    border:
        1px solid rgba(255,255,255,0.20);

    backdrop-filter:
        blur(25px) saturate(160%);

    -webkit-backdrop-filter:
        blur(25px) saturate(160%);

    box-shadow:
        inset 0 1px rgba(255,255,255,0.25),
        0 12px 35px rgba(0,0,0,0.18);
}

[data-testid="stMetricLabel"] {

    color:
        rgba(255,255,255,0.55) !important;
}

[data-testid="stMetricValue"] {

    color:
        rgba(255,255,255,0.95) !important;
}

/* ==========================================================
   STATUS PILL
   ========================================================== */

.status {

    display: inline-block;

    padding: 7px 13px;

    border-radius: 50px;

    background:
        rgba(255,255,255,0.10);

    border:
        1px solid rgba(255,255,255,0.20);

    color:
        rgba(255,255,255,0.75);

    font-size: 12px;

    backdrop-filter:
        blur(20px);
}

/* ==========================================================
   DIVIDER
   ========================================================== */

hr {

    border: none !important;

    height: 1px !important;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(255,255,255,0.20),
            transparent
        ) !important;
}

/* ==========================================================
   SCROLLBAR
   ========================================================== */

::-webkit-scrollbar {
    width: 7px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {

    background:
        rgba(255,255,255,0.18);

    border-radius: 20px;
}

/* ==========================================================
   MOBILE
   ========================================================== */

@media (max-width: 768px) {

    .block-container {
        padding: 20px;
    }

    .hero-title {
        font-size: 32px;
    }

    .hero {
        padding: 28px;
        border-radius: 27px;
    }

    .glass-card {
        border-radius: 21px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

    <div class="hero-light"></div>

    <div class="hero-title">
        ✦ Liquid Glass AI
    </div>

    <div class="hero-subtitle">
        Intelligent requirements analysis with a premium
        translucent interface inspired by modern glass UI.
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# INPUT AREA
# ============================================================

st.markdown(
    '<div class="section-title">Project Requirements</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    project_name = st.text_input(
        "Project Name",
        placeholder="e.g. AI Requirements Engineering Agent"
    )

with col2:
    project_type = st.selectbox(
        "Project Type",
        [
            "AI / Machine Learning",
            "Web Application",
            "Mobile Application",
            "IoT System",
            "Cyber Security",
            "Other"
        ]
    )

requirements = st.text_area(
    "Requirements",
    placeholder=(
        "Paste your software requirements here...\n\n"
        "Example:\n"
        "The system should provide fast login.\n"
        "Users can access the dashboard.\n"
        "The system should store user information."
    ),
    height=180
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("✦  Analyze Requirements"):

    if not requirements.strip():

        st.warning("Please enter your requirements first.")

    else:

        st.success("Requirements submitted successfully.")


# ============================================================
# ANALYSIS CARDS
# ============================================================

st.markdown(
    '<div class="section-title">AI Analysis</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="glass-card">

        <div class="glass-icon">◇</div>

        <div class="card-title">
            Ambiguity
        </div>

        <div class="card-text">
            Detect vague and unclear statements that
            require precise definitions.
        </div>

    </div>
    """, unsafe_allow_html=True)


with c2:
    st.markdown("""
    <div class="glass-card">

        <div class="glass-icon">◈</div>

        <div class="card-title">
            Contradictions
        </div>

        <div class="card-text">
            Identify conflicting requirements and
            incompatible system expectations.
        </div>

    </div>
    """, unsafe_allow_html=True)


with c3:
    st.markdown("""
    <div class="glass-card">

        <div class="glass-icon">◎</div>

        <div class="card-title">
            Duplicates
        </div>

        <div class="card-text">
            Find duplicate and semantically overlapping
            requirement statements.
        </div>

    </div>
    """, unsafe_allow_html=True)


with c4:
    st.markdown("""
    <div class="glass-card">

        <div class="glass-icon">⌘</div>

        <div class="card-title">
            Dependencies
        </div>

        <div class="card-text">
            Discover relationships and dependencies
            between individual requirements.
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# DASHBOARD
# ============================================================

st.markdown(
    '<div class="section-title">Requirement Dashboard</div>',
    unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "Requirements",
        "24",
        "+6"
    )

with m2:
    st.metric(
        "Issues Found",
        "08",
        "-2"
    )

with m3:
    st.metric(
        "Dependencies",
        "12",
        "+4"
    )

with m4:
    st.metric(
        "Clarity Score",
        "87%",
        "+9%"
    )


# ============================================================
# RESULTS
# ============================================================

st.markdown(
    '<div class="section-title">Analysis Results</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1.5, 1])


with left:

    st.markdown("""
    <div class="liquid-glass" style="padding:28px;">

        <div class="card-title">
            Requirement Findings
        </div>

        <br>

        <div class="glass-card">

            <span class="status">
                AMBIGUITY DETECTED
            </span>

            <br><br>

            <div class="card-title">
                Requirement #04
            </div>

            <div class="card-text">

                <b>Original:</b><br>
                "The system should provide fast authentication."

                <br><br>

                <b>Issue:</b><br>
                The term "fast" does not define a measurable
                performance requirement.

                <br><br>

                <b>Suggested:</b><br>
                Authentication should complete within
                2 seconds under normal system load.

            </div>

        </div>

        <br>

        <div class="glass-card">

            <span class="status">
                DEPENDENCY
            </span>

            <br><br>

            <div class="card-title">
                Requirement #11
            </div>

            <div class="card-text">

                A dependency was identified between
                Requirement #07 and Requirement #11.

                <br><br>

                Authentication
                <b>→</b>
                User Dashboard

            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)


with right:

    st.markdown("""
    <div class="liquid-glass" style="padding:28px;">

        <div class="card-title">
            ✦ AI Insights
        </div>

        <br>

        <div class="glass-card">

            <div class="glass-icon">
                ✦
            </div>

            <div class="card-title">
                Recommendation
            </div>

            <div class="card-text">
                Add measurable acceptance criteria
                to improve requirement testability.
            </div>

        </div>

        <br>

        <div class="glass-card">

            <div class="glass-icon">
                ◇
            </div>

            <div class="card-title">
                Traceability
            </div>

            <div class="card-text">
                Every detected issue remains connected
                to its original requirement.
            </div>

        </div>

        <br>

        <div class="glass-card">

            <div class="glass-icon">
                ✓
            </div>

            <div class="card-title">
                Quality
            </div>

            <div class="card-text">
                Requirements are evaluated for clarity,
                consistency and completeness.
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<br><br>

<div style="
    text-align:center;
    color:rgba(255,255,255,0.35);
    font-size:12px;
    padding:20px;
">
    Liquid Glass Interface • Streamlit
</div>
""", unsafe_allow_html=True)
