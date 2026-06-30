import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, require_auth

st.set_page_config(page_title="Risk Factors", page_icon="🩺", layout="wide")
require_auth()

df = load_data()

st.title("🩺 Clinical Risk Factors")
st.caption("Relationship between stroke and hypertension, heart disease, glucose level, BMI, and smoking status.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Stroke Rate: Hypertension")
    g = df.groupby("hypertension_label", observed=True)["stroke"].mean().reset_index()
    g["stroke_rate_%"] = g["stroke"] * 100
    fig = px.bar(g, x="hypertension_label", y="stroke_rate_%", text_auto=".1f",
                 color="hypertension_label", color_discrete_sequence=["#4C9F70", "#D64545"])
    fig.update_layout(xaxis_title="Hypertension", yaxis_title="Stroke Rate (%)", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Stroke Rate: Heart Disease")
    g2 = df.groupby("heart_disease_label", observed=True)["stroke"].mean().reset_index()
    g2["stroke_rate_%"] = g2["stroke"] * 100
    fig2 = px.bar(g2, x="heart_disease_label", y="stroke_rate_%", text_auto=".1f",
                  color="heart_disease_label", color_discrete_sequence=["#4C9F70", "#D64545"])
    fig2.update_layout(xaxis_title="Heart Disease", yaxis_title="Stroke Rate (%)", showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

col3, col4 = st.columns(2)
with col3:
    st.subheader("Avg. Glucose Level by Stroke Outcome")
    fig3 = px.box(df, x="stroke_label", y="avg_glucose_level", color="stroke_label",
                  color_discrete_map={"No Stroke": "#4C9F70", "Stroke": "#D64545"})
    fig3.update_layout(xaxis_title="", yaxis_title="Avg. Glucose Level", showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("BMI by Stroke Outcome")
    fig4 = px.box(df, x="stroke_label", y="bmi", color="stroke_label",
                  color_discrete_map={"No Stroke": "#4C9F70", "Stroke": "#D64545"})
    fig4.update_layout(xaxis_title="", yaxis_title="BMI", showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

col5, col6 = st.columns(2)
with col5:
    st.subheader("Stroke Rate by Glucose Category")
    g5 = df.groupby("glucose_category", observed=True)["stroke"].mean().reset_index()
    g5["stroke_rate_%"] = g5["stroke"] * 100
    fig5 = px.bar(g5, x="glucose_category", y="stroke_rate_%", text_auto=".1f", color="stroke_rate_%",
                  color_continuous_scale="Reds")
    fig5.update_layout(xaxis_title="Glucose Category", yaxis_title="Stroke Rate (%)", coloraxis_showscale=False)
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.subheader("Stroke Rate by Smoking Status")
    g6 = df.groupby("smoking_status", observed=True)["stroke"].mean().reset_index()
    g6["stroke_rate_%"] = g6["stroke"] * 100
    fig6 = px.bar(g6, x="smoking_status", y="stroke_rate_%", text_auto=".1f", color="stroke_rate_%",
                  color_continuous_scale="Reds")
    fig6.update_layout(xaxis_title="Smoking Status", yaxis_title="Stroke Rate (%)", coloraxis_showscale=False)
    st.plotly_chart(fig6, use_container_width=True)

st.divider()
st.subheader("Correlation Heatmap (Numeric & Binary Clinical Variables)")
num_cols = ["age", "hypertension", "heart_disease", "avg_glucose_level", "bmi", "stroke"]
corr = df[num_cols].corr()
fig7 = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1, aspect="auto")
st.plotly_chart(fig7, use_container_width=True)

st.markdown(
    "**Insight:** Hypertension and heart disease roughly double or triple the observed stroke rate. "
    "Elevated glucose (diabetic range) and higher BMI are also associated with increased stroke risk, "
    "though age remains the strongest single correlate in this dataset."
)
