import streamlit as st
import pandas as pd
import plotly.express as px

from model import predict_emotion
from database import save_review, get_reviews, clear_reviews, init_db
from auth import init_auth_db, register_user, login_user

# INIT
init_db()
init_auth_db()

# PAGE CONFIG
st.set_page_config(
    page_title="EmotionSense AI",
    page_icon="🧠",
    layout="wide"
)

# SESSION STATE
if "user" not in st.session_state:
    st.session_state.user = None

# ================= LOGIN PAGE =================
if st.session_state.user is None:

    st.markdown(
        """
        <div style="text-align:center; padding-top:30px;">
            <h1>EmotionSense AI</h1>
            <p style="color:gray; font-size:16px;">
                AI-Powered Emotion Detection & Analytics Platform
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    mode = st.radio("Choose Action", ["Login", "Register"], horizontal=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        if mode == "Register":
            if st.button("Sign Up", use_container_width=True):
                if register_user(username, password):
                    st.success("Account created successfully!")
                else:
                    st.error("Username already exists")

        else:
            if st.button("Login", use_container_width=True):
                user = login_user(username, password)

                if user:
                    st.session_state.user = username
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    st.markdown("---")
    st.caption("© EmotionSense AI | Secure AI Analytics Platform")

# ================= DASHBOARD =================
else:

    # SIDEBAR
    with st.sidebar:

        st.title(f"👤 {st.session_state.user}")

        st.markdown("---")

        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()

        if st.button("Clear Data"):
            clear_reviews(st.session_state.user)
            st.success("Your data has been cleared")

        st.markdown("---")
        st.caption("EmotionSense AI v1.0")

    # MAIN TITLE
    st.title("EmotionSense Dashboard")
    st.caption("Real-time Emotion Detection & Analytics System")

    # INPUT SECTION
    st.markdown("### Analyze Text")

    text = st.text_area(
        "Enter your text here...",
        height=120
    )

    if st.button("Analyze Emotion"):

        if text.strip():

            emotion, confidence = predict_emotion(text)

            save_review(
                st.session_state.user,
                text,
                emotion,
                confidence
            )

            st.success(
                f"Detected Emotion: {emotion.upper()}"
            )

            st.info(
                f"Confidence Score: {confidence:.2%}"
            )

        else:
            st.warning(
                "Please enter some text"
            )

    st.markdown("---")

    # USER-SPECIFIC DATA
    data = get_reviews(
        st.session_state.user
    )

    if data:

        df = pd.DataFrame(
            data,
            columns=[
                "Text",
                "Emotion",
                "Confidence"
            ]
        )

        # METRICS
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Entries",
            len(df)
        )

        col2.metric(
            "Top Emotion",
            df["Emotion"].mode()[0]
        )

        col3.metric(
            "Avg Confidence",
            round(
                df["Confidence"].mean(),
                2
            )
        )

        st.markdown("---")

        # CHARTS
        col1, col2 = st.columns(2)

        with col1:

            fig1 = px.pie(
                df,
                names="Emotion",
                title="Emotion Distribution"
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

        with col2:

            fig2 = px.bar(
                df["Emotion"].value_counts(),
                title="Emotion Count"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

        st.markdown("---")

        # HISTORY
        st.subheader("Emotion History")

        st.dataframe(
            df,
            use_container_width=True,
            height=350
        )

    else:

        st.info(
            "No data available. Start analyzing emotions!"
        )