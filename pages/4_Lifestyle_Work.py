import streamlit as st
import plotly.express as px
from utils import load_data, require_auth

st.set_page_config(page_title="Lifestyle & Work", page_icon="🏙️", layout="wide")
require_auth()

df = load_data()

st.title("🏙️ Lifestyle & Work Patterns")
st.caption("Stroke prevalence by work type, residence setting, and marital status.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Stroke Rate by Work Type")
    g = df.groupby("work_type", observed=True)["stroke"].mean().reset_index()
    g["stroke_rate_%"] = g["stroke"] * 100
    g = g.sort_values("stroke_rate_%", ascending=False)
    fig = px.bar(g, x="work_type", y="stroke_rate_%", text_auto=".1f", color="stroke_rate_%",
                 color_continuous_scale="Reds")
    fig.update_layout(xaxis_title="Work Type", yaxis_title="Stroke Rate (%)", coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Stroke Rate by Residence Type")
    g2 = df.groupby("Residence_type", observed=True)["stroke"].mean().reset_index()
    g2["stroke_rate_%"] = g2["stroke"] * 100
    fig2 = px.bar(g2, x="Residence_type", y="stroke_rate_%", text_auto=".1f",
                  color="Residence_type", color_discrete_sequence=px.colors.qualitative.Set2)
    fig2.update_layout(xaxis_title="Residence Type (Geographic Proxy)", yaxis_title="Stroke Rate (%)", showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

col3, col4 = st.columns(2)
with col3:
    st.subheader("Stroke Rate by Marital Status")
    g3 = df.groupby("ever_married", observed=True)["stroke"].mean().reset_index()
    g3["stroke_rate_%"] = g3["stroke"] * 100
    fig3 = px.bar(g3, x="ever_married", y="stroke_rate_%", text_auto=".1f",
                  color="ever_married", color_discrete_sequence=["#4C9F70", "#D64545"])
    fig3.update_layout(xaxis_title="Ever Married", yaxis_title="Stroke Rate (%)", showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Patient Count by Work Type & Stroke Outcome")
    fig4 = px.histogram(df, x="work_type", color="stroke_label", barmode="group",
                         color_discrete_map={"No Stroke": "#4C9F70", "Stroke": "#D64545"})
    fig4.update_layout(xaxis_title="Work Type", yaxis_title="Count")
    st.plotly_chart(fig4, use_container_width=True)

st.markdown(
    "**Insight:** Self-employed patients show the highest stroke rate, consistent with this group "
    "skewing older on average. Marital status ('ever married') shows a notable gap, again largely "
    "explained by the underlying age distribution rather than marriage itself. Urban vs. rural "
    "residence shows minimal difference, suggesting geography is not a strong driver in this dataset."
)
