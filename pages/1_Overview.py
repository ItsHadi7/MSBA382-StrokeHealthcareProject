import streamlit as st
import plotly.express as px
from utils import load_data, require_auth

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")
require_auth()

df = load_data()

st.title("📊 Overview")
st.caption("Key metrics across the full patient population, filterable by demographic and clinical attributes.")

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")
gender_sel = st.sidebar.multiselect("Gender", sorted(df["gender"].unique()), default=sorted(df["gender"].unique()))
age_sel = st.sidebar.slider("Age range", int(df["age"].min()), int(df["age"].max()), (0, 100))
hyp_sel = st.sidebar.multiselect("Hypertension", sorted(df["hypertension_label"].unique()), default=sorted(df["hypertension_label"].unique()))
heart_sel = st.sidebar.multiselect("Heart Disease", sorted(df["heart_disease_label"].unique()), default=sorted(df["heart_disease_label"].unique()))
smoke_sel = st.sidebar.multiselect("Smoking Status", sorted(df["smoking_status"].unique()), default=sorted(df["smoking_status"].unique()))
work_sel = st.sidebar.multiselect("Work Type", sorted(df["work_type"].unique()), default=sorted(df["work_type"].unique()))
resid_sel = st.sidebar.multiselect("Residence Type", sorted(df["Residence_type"].unique()), default=sorted(df["Residence_type"].unique()))

fdf = df[
    df["gender"].isin(gender_sel)
    & df["age"].between(age_sel[0], age_sel[1])
    & df["hypertension_label"].isin(hyp_sel)
    & df["heart_disease_label"].isin(heart_sel)
    & df["smoking_status"].isin(smoke_sel)
    & df["work_type"].isin(work_sel)
    & df["Residence_type"].isin(resid_sel)
]

st.sidebar.markdown(f"**{len(fdf):,} patients** match current filters")

# ---------- KPIs ----------
total = len(fdf)
stroke_count = int(fdf["stroke"].sum())
stroke_rate = (stroke_count / total * 100) if total else 0
avg_age = fdf["age"].mean() if total else 0
avg_glucose = fdf["avg_glucose_level"].mean() if total else 0
avg_bmi = fdf["bmi"].mean() if total else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Patients", f"{total:,}")
c2.metric("Stroke Cases", f"{stroke_count:,}")
c3.metric("Stroke Rate", f"{stroke_rate:.1f}%")
c4.metric("Avg. Age", f"{avg_age:.1f}")
c5.metric("Avg. BMI", f"{avg_bmi:.1f}")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Stroke Outcome Distribution")
    fig = px.pie(fdf, names="stroke_label", hole=0.45, color="stroke_label",
                 color_discrete_map={"No Stroke": "#4C9F70", "Stroke": "#D64545"})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Patients by Gender")
    fig2 = px.histogram(fdf, x="gender", color="stroke_label", barmode="group",
                         color_discrete_map={"No Stroke": "#4C9F70", "Stroke": "#D64545"})
    fig2.update_layout(yaxis_title="Count", xaxis_title="Gender")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.subheader("Filtered Data Preview")
st.dataframe(fdf.drop(columns=["age_group", "stroke_label", "hypertension_label", "heart_disease_label", "bmi_category", "glucose_category"]), use_container_width=True, height=300)
