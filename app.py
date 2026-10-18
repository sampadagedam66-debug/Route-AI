import os

import streamlit as st
from dotenv import load_dotenv
from google import genai


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

# Swap this for any travel photo you like. If it fails to load,
# the dark gradient underneath is shown instead.
BACKGROUND_URL = (
    "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1"
    "?auto=format&fit=crop&w=2000&q=80"
)

COLD_PLACES = [
    "manali", "shimla", "leh", "ladakh", "kashmir", "spiti", "auli",
    "switzerland", "alps", "iceland", "norway", "finland", "himalaya",
]

# Indicative share of spending by budget style (percent). Not live prices.
BUDGET_SPLIT = {
    "Budget-friendly": [35, 25, 15, 15, 10],
    "Moderate": [40, 25, 10, 15, 10],
    "Premium": [50, 20, 10, 15, 5],
}
SPLIT_LABELS = [
    "Stay",
    "Food",
    "Transport",
    "Activities",
    "Extras",
]

st.set_page_config(
    page_title="Route AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM DESIGN
# ============================================================

CSS = """
<style>

    /* Realistic photo background with a dark overlay for readability */
    .stApp {
        background-color: #07111f;
        background-image:
            linear-gradient(
                180deg,
                rgba(5, 14, 26, 0.50) 0%,
                rgba(5, 14, 26, 0.80) 55%,
                rgba(5, 14, 26, 0.95) 100%
            ),
            url("__BACKGROUND_URL__");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #f5f7fa;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* Main container */
    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Hero section */
    .hero {
        padding: 2.5rem 1rem 2rem 1rem;
        text-align: center;
    }

    .hero-badge {
        display: inline-block;
        padding: 0.45rem 1rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.18);
        font-size: 0.85rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(8px);
    }

    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        letter-spacing: -2px;
        margin: 0;
        background: linear-gradient(90deg, #ffffff, #8ee9ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: #d3deea;
        margin-top: 0.8rem;
        text-shadow: 0 2px 12px rgba(0,0,0,0.5);
    }

    /* Feature cards */
    .feature-card {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 18px;
        padding: 1.2rem;
        height: 150px;
        backdrop-filter: blur(12px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .feature-card:hover {
        transform: translateY(-4px);
        border-color: rgba(142,233,255,0.55);
    }

    .feature-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-top: 0.5rem;
    }

    .feature-text {
        color: #c3d1e0;
        font-size: 0.9rem;
    }

    /* Glass containers (st.container with a key) */
    .st-key-planner,
    .st-key-result,
    .st-key-budget,
    .st-key-refine {
        background: rgba(8, 20, 36, 0.58);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 22px;
        padding: 1.6rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.30);
    }

    .st-key-result {
        border-left: 4px solid #6ddcff;
    }

    /* Section headings */
    .section-title {
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 1rem;
        text-shadow: 0 2px 12px rgba(0,0,0,0.5);
    }

    /* Form widgets */
    [data-testid="stWidgetLabel"] p,
    label p {
        color: #dbe7f3 !important;
    }

    .stTextInput input,
    div[data-baseweb="select"] > div,
    div[data-baseweb="base-input"] {
        background: rgba(7, 17, 31, 0.65) !important;
        color: #f5f7fa !important;
        border-color: rgba(255,255,255,0.18) !important;
    }

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button {
        background: linear-gradient(90deg, #2c7be5, #00b4be);
        color: #ffffff;
        border: 0;
        border-radius: 14px;
        font-weight: 700;
        padding: 0.75rem 1rem;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 28px rgba(0,180,190,0.35);
        color: #ffffff;
    }

    /* Budget metrics */
    [data-testid="stMetricValue"] {
        color: #8ee9ff;
    }

    [data-testid="stMetricLabel"] p {
        color: #dbe7f3 !important;
    }

    /* Footer */
    .custom-footer {
        text-align: center;
        color: #9db0c4;
        margin-top: 3rem;
        font-size: 0.85rem;
    }

</style>
"""

st.markdown(
    CSS.replace("__BACKGROUND_URL__", BACKGROUND_URL),
    unsafe_allow_html=True
)


# ============================================================
# API SETUP
# ============================================================

if not API_KEY:
    st.error(
        "Gemini API key was not found. "
        "Please check your .env file."
    )
    st.stop()

client = genai.Client(api_key=API_KEY)


def ask_gemini(prompt):
    """Send a prompt to Gemini and return the text reply."""
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text


def show_error(error):
    """Show a friendly error with a hint about the usual causes."""
    st.error("Route AI couldn't complete that request.")
    st.info(
        "If the error mentions API key, check your GEMINI_API_KEY. "
        "If it mentions quota or 429, you have hit a usage limit. "
        "If it mentions 403, the API key/project has an access problem."
    )
    st.caption(f"Technical details: {error}")


def wants_snow(destination_text, selected_interests):
    """Snow for mountain / cold-place trips, balloons for everything else."""
    name = destination_text.lower()
    return (
        "Mountains" in selected_interests
        or any(place in name for place in COLD_PLACES)
    )


# ============================================================
# SESSION STATE
# ============================================================

st.session_state.setdefault("itinerary", "")
st.session_state.setdefault("trip_destination", "")
st.session_state.setdefault("trip_budget", "Moderate")


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="hero">'
    '<div class="hero-badge">AI-Powered Travel Planning</div>'
    '<div class="hero-title">Route AI</div>'
    '<div class="hero-subtitle">'
    'Your intelligent companion for planning meaningful journeys.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# FEATURES
# ============================================================

feature_1, feature_2, feature_3, feature_4 = st.columns(4)

with feature_1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">Smart Itineraries</div>
        <div class="feature-text">
            Get a personalized day-by-day travel plan.
        </div>
    </div>
    """, unsafe_allow_html=True)

with feature_2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">Budget Aware</div>
        <div class="feature-text">
            Plan and see how your spending usually splits.
        </div>
    </div>
    """, unsafe_allow_html=True)

with feature_3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">Stay & Transport</div>
        <div class="feature-text">
            Get accommodation and local transport ideas.
        </div>
    </div>
    """, unsafe_allow_html=True)

with feature_4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">Refine Your Plan</div>
        <div class="feature-text">
            Ask for changes and your itinerary updates instantly.
        </div>
    </div>
    """, unsafe_allow_html=True)


st.write("")


# ============================================================
# TRIP PLANNER
# ============================================================

st.markdown(
    '<div class="section-title">Design Your Journey</div>',
    unsafe_allow_html=True
)

with st.container(key="planner"):

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        destination = st.text_input(
            "Destination",
            placeholder="e.g. Goa, Manali, Paris..."
        )

    with row1_col2:
        duration = st.slider(
            "Trip duration",
            min_value=1,
            max_value=30,
            value=4
        )

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        budget = st.selectbox(
            "Budget preference",
            [
                "Budget-friendly",
                "Moderate",
                "Premium"
            ]
        )

    with row2_col2:
        travel_style = st.selectbox(
            "Travel style",
            [
                "Balanced",
                "Adventure",
                "Relaxation",
                "Culture & History",
                "Food & Cafés",
                "Nature & Wildlife",
                "Photography"
            ]
        )

    row3_col1, row3_col2 = st.columns(2)

    with row3_col1:
        travelers = st.selectbox(
            "Traveling with",
            [
                "Solo",
                "Friends",
                "Family",
                "Partner"
            ]
        )

    with row3_col2:
        interests = st.multiselect(
            "Your interests",
            [
                "Beaches",
                "Mountains",
                "Historical places",
                "Local food",
                "Shopping",
                "Nightlife",
                "Photography",
                "Nature",
                "Local experiences"
            ]
        )

    st.markdown("### Trip Details")

    new_col1, new_col2 = st.columns(2)

    with new_col1:
        accommodation = st.selectbox(
            "Accommodation preference",
            [
                "No specific preference",
                "Budget hostel / guesthouse",
                "Mid-range hotel",
                "Premium hotel / resort",
                "Homestay / local stay"
            ]
        )

    with new_col2:
        transport = st.selectbox(
            "Local transport preference",
            [
                "No specific preference",
                "Public transport",
                "Taxi / cab",
                "Rental vehicle",
                "Walking + public transport",
                "Mix of available options"
            ]
        )

    st.markdown(
        """
        <p style="color:#c3d1e0; font-size:0.9rem; margin-top:0.4rem;">
            Route AI will use these preferences to personalize your stay,
            transportation suggestions, and packing checklist.
        </p>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# GENERATE BUTTON
# ============================================================

generate = st.button(
    "Create My Journey",
    use_container_width=True
)


# ============================================================
# AI GENERATION
# ============================================================

if generate:

    if not destination.strip():

        st.warning(
            "Please enter a destination before creating your journey."
        )

    else:

        selected_interests = (
            ", ".join(interests)
            if interests
            else "General exploration"
        )

        prompt = f"""
You are Route AI, an intelligent and practical travel planning assistant.

Create a personalized travel plan using the following information:

Destination: {destination}
Trip duration: {duration} days
Budget style: {budget}
Travel style: {travel_style}
Traveling with: {travelers}
Interests: {selected_interests}
Accommodation preference: {accommodation}
Local transport preference: {transport}

IMPORTANT:
- Keep recommendations realistic and practical.
- Do not pretend to know live prices, availability, or current conditions.
- Do not claim that a hotel, restaurant, attraction, or transport service
  is currently available unless the user has provided that information.
- Give approximate guidance rather than fake exact prices.
- Avoid overcrowding each day with too many activities.
- Consider the selected budget, travel style, group type, interests,
  accommodation preference, and transport preference.

Create the response with these sections:

# Trip Overview

Give a short overview of the journey and explain why the plan fits
the traveler's preferences.

# Day-by-Day Itinerary

For every day provide:

Morning:
Afternoon:
Evening:

Keep the schedule realistic and group nearby activities together where possible.

# Accommodation Suggestions

Suggest suitable types of accommodation and useful areas or neighborhoods
to consider.

Explain why each type/area may fit the selected budget and travel style.

Do not invent hotel availability or exact current prices.

# Transport Planner

Explain practical ways to get around the destination.

Include:
- Getting around locally
- Best option for the traveler's preferences
- When walking, public transport, taxi, or rental may be useful
- General transport tips

Do not claim live schedules or current fares.

# Local Food & Experiences

Suggest local foods, experiences, or cultural activities that match
the traveler's interests.

# Budget Guidance

Explain how the traveler can generally divide spending between:

- Accommodation
- Food
- Local transport
- Activities
- Extra expenses

Use broad estimates or relative categories rather than pretending
to know live prices.

# Smart Packing List

Create a practical packing checklist based on:

- Destination
- Trip duration
- Travel style
- Interests
- Activities mentioned in the itinerary

Group the list into useful categories such as:

- Essentials
- Clothing
- Electronics
- Personal items
- Activity-specific items

# Smart Travel Tips

Give 5 useful destination-specific general travel tips.

# Hidden Gem Idea

Suggest one less-obvious experience or place worth exploring.

End with a short section called:

# Route AI Summary

Summarize the trip in 4-6 concise bullet points.

Keep the response clear, practical, and easy for a student traveler
to understand.
"""

        with st.spinner(
            "Route AI is designing your journey..."
        ):

            try:

                st.session_state.itinerary = ask_gemini(prompt)
                st.session_state.trip_destination = destination.strip()
                st.session_state.trip_budget = budget

                # Celebration effect once the journey is ready
                if wants_snow(destination, interests):
                    st.snow()
                else:
                    st.balloons()

            except Exception as error:

                show_error(error)


# ============================================================
# DISPLAY SAVED RESULT
# ============================================================

if st.session_state.itinerary:

    st.divider()

    st.markdown(
        '<div class="section-title">'
        'Your Personalized Journey'
        '</div>',
        unsafe_allow_html=True
    )

    with st.container(key="result"):
        st.markdown(st.session_state.itinerary)


    # ========================================================
    # BUDGET SPLIT
    # ========================================================

    with st.container(key="budget"):

        st.markdown("### Budget Split at a Glance")

        shares = BUDGET_SPLIT[st.session_state.trip_budget]

        split_columns = st.columns(len(SPLIT_LABELS))

        for column, label, share in zip(
            split_columns, SPLIT_LABELS, shares
        ):
            column.metric(label, f"{share}%")
            column.progress(share / 100)

        st.caption(
            f"Indicative spending split for a "
            f"{st.session_state.trip_budget.lower()} trip. "
            "These are general shares, not live prices."
        )


    # ========================================================
    # REFINE YOUR JOURNEY
    # ========================================================

    with st.container(key="refine"):

        st.markdown("### Refine Your Journey")

        tweak = st.text_input(
            "What would you like to change?",
            placeholder="e.g. Make day 2 more relaxed, add more food spots...",
            key="tweak_input"
        )

        if st.button("Update Itinerary", use_container_width=True):

            if not tweak.strip():

                st.warning(
                    "Tell Route AI what to change first."
                )

            else:

                refine_prompt = f"""
You are Route AI, a practical travel planning assistant.

Below is an existing travel itinerary. Update it based on the
traveler's request and return the COMPLETE updated itinerary in the
same format, headings, and style. Keep everything the request does not
affect. Do not pretend to know live prices or availability.

Traveler's request:
{tweak}

Current itinerary:
{st.session_state.itinerary}
"""

                with st.spinner("Route AI is updating your journey..."):

                    try:

                        st.session_state.itinerary = ask_gemini(
                            refine_prompt
                        )
                        st.rerun()

                    except Exception as error:

                        show_error(error)


    # ========================================================
    # DOWNLOAD ITINERARY / START A NEW JOURNEY
    # ========================================================

    st.markdown("### Save Your Journey")

    filename_destination = (
        st.session_state.trip_destination
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )

    download_filename = (
        f"route_ai_{filename_destination}_itinerary.txt"
    )

    action_col1, action_col2 = st.columns(2)

    with action_col1:
        st.download_button(
            label="Download Itinerary",
            data=st.session_state.itinerary,
            file_name=download_filename,
            mime="text/plain",
            use_container_width=True
        )

    with action_col2:
        # Clears the current plan so a fresh trip can be started
        if st.button("Start a New Journey", use_container_width=True):
            st.session_state.itinerary = ""
            st.session_state.trip_destination = ""
            st.rerun()

    st.caption(
        "Save your personalized Route AI itinerary as a text file "
        "for later reference."
    )


# ============================================================
# FOOTER
# ===================================================