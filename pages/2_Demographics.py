import streamlit as st
import plotly.express as px
from utils import load_data, require_auth

st.set_page_config(page_title="Demographics", page_icon="🧑‍🤝‍🧑", layout="wide")
require_auth()

df = load_data()

st.title("🧑‍🤝‍🧑 Demographics: Age & Gender")
st.caption("How stroke prevalence varies across age groups and gender.")

st.sidebar.header("Filters")
gender_sel = st.sidebar.multiselect("Gender", sorted(df["gender"].unique()), default=sorted(df["gender"].unique()))
fdf = df[df["gender"].isin(gender_sel)]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Stroke Rate by Age Group")
    rate_by_age = fdf.groupby("age_group", observed=True)["stroke"].mean().reset_index()
    rate_by_age["stroke_rate_%"] = rate_by_age["stroke"] * 100
    fig = px.bar(rate_by_age, x="age_group", y="stroke_rate_%", text_auto=".1f",
                 color="stroke_rate_%", color_continuous_scale="Reds")
    fig.update_layout(yaxis_title="Stroke Rate (%)", xaxis_title="Age Group", coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Stroke Rate by Gender")
    rate_by_gender = fdf.groupby("gender", observed=True)["stroke"].mean().reset_index()
    rate_by_gender["stroke_rate_%"] = rate_by_gender["stroke"] * 100
    fig2 = px.bar(rate_by_gender, x="gender", y="stroke_rate_%", text_auto=".1f",
                  color="gender", color_discrete_sequence=px.colors.qualitative.Set2)
    fig2.update_layout(yaxis_title="Stroke Rate (%)", xaxis_title="Gender")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.subheader("Age Distribution by Stroke Outcome")
fig3 = px.histogram(fdf, x="age", color="stroke_label", barmode="overlay", nbins=40, opacity=0.65,
                     color_discrete_map={"No Stroke": "#4C9F70", "Stroke": "#D64545"})
fig3.update_layout(xaxis_title="Age", yaxis_title="Count")
st.plotly_chart(fig3, use_container_width=True)

st.divider()
st.subheader("Stroke Count Heatmap — Age Group vs Gender")
heat = fdf.groupby(["age_group", "gender"], observed=True)["stroke"].sum().reset_index()
heat_pivot = heat.pivot(index="age_group", columns="gender", values="stroke").fillna(0)
fig4 = px.imshow(heat_pivot, text_auto=True, color_continuous_scale="Reds", aspect="auto")
fig4.update_layout(xaxis_title="Gender", yaxis_title="Age Group")
st.plotly_chart(fig4, use_container_width=True)

st.markdown(
    "**Insight:** Stroke risk rises sharply with age, with the steepest increase after 60. "
    "Gender differences in raw stroke rate are modest in this dataset, suggesting age is a far "
    "stronger demographic driver than gender alone."
)
