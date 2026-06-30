import pandas as pd
import streamlit as st


@st.cache_data
def load_data(path: str = "data.csv") -> pd.DataFrame:
    df = pd.read_csv(path)

    # Drop the single 'Other' gender row only if it's negligible noise for charts (keep for table, flag for charts)
    df["bmi"] = df["bmi"].fillna(df["bmi"].median())

    # Age bins for grouped analysis
    bins = [0, 18, 30, 45, 60, 75, 100]
    labels = ["0-18", "19-30", "31-45", "46-60", "61-75", "76+"]
    df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=True, include_lowest=True)

    df["stroke_label"] = df["stroke"].map({0: "No Stroke", 1: "Stroke"})
    df["hypertension_label"] = df["hypertension"].map({0: "No", 1: "Yes"})
    df["heart_disease_label"] = df["heart_disease"].map({0: "No", 1: "Yes"})

    bmi_bins = [0, 18.5, 25, 30, 100]
    bmi_labels = ["Underweight", "Normal", "Overweight", "Obese"]
    df["bmi_category"] = pd.cut(df["bmi"], bins=bmi_bins, labels=bmi_labels)

    glu_bins = [0, 100, 125, 1000]
    glu_labels = ["Normal (<100)", "Prediabetic (100-125)", "Diabetic (>125)"]
    df["glucose_category"] = pd.cut(df["avg_glucose_level"], bins=glu_bins, labels=glu_labels)

    return df


def require_auth():
    """Guard for sub-pages so they can't be viewed without passing the Home.py password gate."""
    if not st.session_state.get("authenticated", False):
        st.warning("Please log in from the Home page first.")
        st.stop()
