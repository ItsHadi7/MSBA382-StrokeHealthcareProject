import streamlit as st

st.set_page_config(
    page_title="Stroke Risk Analytics",
    page_icon="🧠",
    layout="wide",
)

# ---------- Simple password gate ----------
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets.get("APP_PASSWORD", "stroke2026"):
            st.session_state["authenticated"] = True
            del st.session_state["password"]
        else:
            st.session_state["authenticated"] = False

    if st.session_state.get("authenticated", False):
        return True

    st.markdown(
        """
        <div style='text-align:center; margin-top:60px;'>
            <h1>🧠 Stroke Risk Analytics</h1>
            <p style='color:gray;'>Consultant Dashboard — Healthcare Analytics Project</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.text_input("Enter password", type="password", on_change=password_entered, key="password")
        if st.session_state.get("authenticated") is False:
            st.error("Incorrect password. Please try again.")
    return False


if not check_password():
    st.stop()

# ---------- Landing page content (after auth) ----------
st.title("🧠 Stroke Risk Analytics Dashboard")
st.caption("Consultant-to-Client Dashboard | Healthcare Analytics Engagement")

st.markdown(
    """
Welcome. This dashboard was prepared to help the healthcare facility understand
the burden of **stroke** among its patient population, identify the demographic
and clinical risk factors most associated with stroke, and provide a tool to
estimate individual stroke risk.

### How to navigate
Use the sidebar to move between sections:
- **Overview** — key metrics and data summary
- **Demographics** — stroke distribution by age and gender
- **Risk Factors** — clinical risk factors (hypertension, heart disease, glucose, BMI, smoking)
- **Lifestyle & Work** — work type, residence, marital status patterns
- **Predictive Model** — machine learning model estimating stroke risk from patient attributes

### Data source
Stroke Prediction Dataset (Kaggle), containing 5,110 patient records with demographic,
lifestyle, and clinical attributes, with a binary stroke outcome.
"""
)

st.info("Select a page from the sidebar to begin exploring the data.")
