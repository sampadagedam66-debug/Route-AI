import os

import streamlit as st
from dotenv import load_dotenv
from google import genai


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="Route AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM DESIGN
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(44, 95, 170, 0.35),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(0, 180, 190, 0.20),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #07111f 0%,
                #0b1d31 45%,
                #102c3f 100%
            );
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
        background: transparent;
    }

    .hero-badge {
        display: inline-block;
        padding: 0.45rem 1rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        letter-spacing: -2px;
        margin: 0;
        background: linear-gradient(
            90deg,
            #ffffff,
            #8ee9ff
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: #b8c7d9;
        margin-top: 0.8rem;
    }

    /* Cards */
    .glass-card {
        background: rgba(255,255,255,0.055);
        border: 1px solid rgba(255,255,255,0.11);
        border-radius: 20px;
        padding: 1.4rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(12px);
    }

    .feature-card {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 18px;
        padding: 1.2rem;
        height: 145px;
    }

    .feature-icon {
        font-size: 1.7rem;
    }

    .feature-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-top: 0.5rem;
    }

    .feature-text {
        color: #aebed0;
        font-size: 0.9rem;
    }

    /* Section headings */
    .section-title {
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    /* Result */
    .result-box {
        background: rgba(255,255,255,0.045);
        border-left: 4px solid #6ddcff;
        border-radius: 12px;
        padding: 1.2rem;
        margin-top: 1rem;
    }

    /* Footer */
    .custom-footer {
        text-align: center;
        color: #8092a6;
        margin-top: 3rem;
        font-size: 0.85rem;
    }

</style>
""", unsafe_allow_html=True)


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


# ============================================================
# SESSION STATE
# ============================================================

if "itinerary" not in st.session_state:
    st.session_state.itinerary = ""

if "trip_destination" not in st.session_state:
    st.session_state.trip_destination = ""


# ============================================================
# HERO
# ============================================================

st.html("""
<div class="hero">
    <div class="hero-badge">
        ✦ AI-Powered Travel Planning
    </div>

    <div class="hero-title">
        ✈️ Route AI
    </div>

    <div class="hero-subtitle">
        Your intelligent companion for planning meaningful journeys.
    </div>
</div>
""")


# ============================================================
# FEATURES
# ============================================================

feature_1, feature_2, feature_3, feature_4 = st.columns(4)

with feature_1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🗺️</div>
        <div class="feature-title">Smart Itineraries</div>
        <div class="feature-text">
            Get a personalized day-by-day travel plan.
        </div>
    </div>
    """, unsafe_allow_html=True)

with feature_2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💰</div>
        <div class="feature-title">Budget Aware</div>
        <div class="feature-text">
            Plan according to your preferred spending style.
        </div>
    </div>
    """, unsafe_allow_html=True)

with feature_3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🏨</div>
        <div class="feature-title">Stay & Transport</div>
        <div class="feature-text">
            Get accommodation and local transport ideas.
        </div>
    </div>
    """, unsafe_allow_html=True)

with feature_4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎒</div>
        <div class="feature-title">Smart Packing</div>
        <div class="feature-text">
            Receive a useful packing checklist for your trip.
        </div>
    </div>
    """, unsafe_allow_html=True)


st.write("")


# ============================================================
# TRIP PLANNER
# ============================================================

st.markdown(
    '<div class="section-title">🌍 Design Your Journey</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    destination = st.text_input(
        "📍 Destination",
        placeholder="e.g. Goa, Manali, Paris..."
    )

with row1_col2:
    duration = st.slider(
        "🗓️ Trip duration",
        min_value=1,
        max_value=30,
        value=4
    )


row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    budget = st.selectbox(
        "💰 Budget preference",
        [
            "Budget-friendly",
            "Moderate",
            "Premium"
        ]
    )

with row2_col2:
    travel_style = st.selectbox(
        "🎒 Travel style",
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
        "👥 Traveling with",
        [
            "Solo",
            "Friends",
            "Family",
            "Partner"
        ]
    )

with row3_col2:
    interests = st.multiselect(
        "❤️ Your interests",
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


# ============================================================
# NEW FEATURES
# ============================================================

st.markdown("### 🧳 Trip Details")

new_col1, new_col2 = st.columns(2)

with new_col1:
    accommodation = st.selectbox(
        "🏨 Accommodation preference",
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
        "🚆 Local transport preference",
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
    <p style="color:#aebed0; font-size:0.9rem; margin-top:0.4rem;">
        Route AI will use these preferences to personalize your stay,
        transportation suggestions, and packing checklist.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# GENERATE BUTTON
# ============================================================

generate = st.button(
    "✨ Create My Journey",
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

# ✈️ Trip Overview

Give a short overview of the journey and explain why the plan fits
the traveler's preferences.

# 🗓️ Day-by-Day Itinerary

For every day provide:

Morning:
Afternoon:
Evening:

Keep the schedule realistic and group nearby activities together where possible.

# 🏨 Accommodation Suggestions

Suggest suitable types of accommodation and useful areas or neighborhoods
to consider.

Explain why each type/area may fit the selected budget and travel style.

Do not invent hotel availability or exact current prices.

# 🚆 Transport Planner

Explain practical ways to get around the destination.

Include:
- Getting around locally
- Best option for the traveler's preferences
- When walking, public transport, taxi, or rental may be useful
- General transport tips

Do not claim live schedules or current fares.

# 🍜 Local Food & Experiences

Suggest local foods, experiences, or cultural activities that match
the traveler's interests.

# 💰 Budget Guidance

Explain how the traveler can generally divide spending between:

- Accommodation
- Food
- Local transport
- Activities
- Extra expenses

Use broad estimates or relative categories rather than pretending
to know live prices.

# 🎒 Smart Packing List

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

# 🛡️ Smart Travel Tips

Give 5 useful destination-specific general travel tips.

# ⭐ Hidden Gem Idea

Suggest one less-obvious experience or place worth exploring.

End with a short section called:

# 🧭 Route AI Summary

Summarize the trip in 4-6 concise bullet points.

Keep the response clear, practical, and easy for a student traveler
to understand.
"""

        with st.spinner(
            "Route AI is designing your journey... ✨"
        ):

            try:

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt
                )

                st.session_state.itinerary = response.text
                st.session_state.trip_destination = destination.strip()

            except Exception as error:

                st.error(
                    "Route AI couldn't generate the itinerary."
                )

                st.error(f"Actual error: {error}")

                st.info(
                    "If the error mentions API key, check your GEMINI_API_KEY. "
                    "If it mentions quota or 429, you have hit a usage limit. "
                    "If it mentions 403, the API key/project has an access problem."
                )

                st.caption(
                    f"Technical details: {error}"
                )


# ============================================================
# DISPLAY SAVED RESULT
# ============================================================

if st.session_state.itinerary:

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '🗺️ Your Personalized Journey'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="result-box">',
        unsafe_allow_html=True
    )

    st.markdown(st.session_state.itinerary)

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # DOWNLOAD ITINERARY
    # ========================================================

    st.markdown("### 💾 Save Your Journey")

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

    st.download_button(
        label="📥 Download Itinerary",
        data=st.session_state.itinerary,
        file_name=download_filename,
        mime="text/plain",
        use_container_width=True
    )

    st.caption(
        "Save your personalized Route AI itinerary as a text file "
        "for later reference."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="custom-footer">
    Built with Python • Streamlit • Google Gemini
    <br>
    Route AI — Plan smarter. Explore better. ✈️
</div>
""", unsafe_allow_html=True)
