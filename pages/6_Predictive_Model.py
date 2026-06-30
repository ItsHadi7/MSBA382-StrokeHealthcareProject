import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve, classification_report
from imblearn.over_sampling import SMOTE
from utils import load_data, require_auth

st.set_page_config(page_title="Predictive Model", page_icon="🤖", layout="wide")
require_auth()

df = load_data()

st.title("🤖 Predictive Model: Stroke Risk Estimation")
st.caption("A machine learning model trained to estimate stroke probability from patient attributes. (Bonus component)")

st.warning(
    "⚠️ This model is built for an academic analytics project and is **not** a clinical diagnostic tool. "
    "Stroke is rare in this dataset (~4.9% of patients), so class imbalance techniques (SMOTE) are used."
)

# ---------- Prepare features ----------
features = ["age", "hypertension", "heart_disease", "avg_glucose_level", "bmi",
            "gender", "ever_married", "work_type", "Residence_type", "smoking_status"]
model_df = df[features + ["stroke"]].copy()
model_df = pd.get_dummies(model_df, columns=["gender", "ever_married", "work_type", "Residence_type", "smoking_status"], drop_first=True)

X = model_df.drop(columns=["stroke"])
y = model_df["stroke"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

sm = SMOTE(random_state=42)
X_train_res, y_train_res = sm.fit_resample(X_train_scaled, y_train)

model_choice = st.sidebar.radio("Model", ["Logistic Regression", "Random Forest"])

if model_choice == "Logistic Regression":
    model = LogisticRegression(max_iter=1000, random_state=42)
else:
    model = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42)

model.fit(X_train_res, y_train_res)
y_pred = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)[:, 1]

auc = roc_auc_score(y_test, y_proba)

st.subheader("Model Performance")
c1, c2, c3 = st.columns(3)
c1.metric("Model", model_choice)
c2.metric("ROC-AUC", f"{auc:.3f}")
c3.metric("Test Set Size", f"{len(y_test):,}")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Confusion Matrix**")
    cm = confusion_matrix(y_test, y_pred)
    fig_cm = px.imshow(cm, text_auto=True, color_continuous_scale="Blues",
                        labels=dict(x="Predicted", y="Actual"),
                        x=["No Stroke", "Stroke"], y=["No Stroke", "Stroke"])
    st.plotly_chart(fig_cm, use_container_width=True)

with col2:
    st.markdown("**ROC Curve**")
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    fig_roc = px.area(x=fpr, y=tpr, labels=dict(x="False Positive Rate", y="True Positive Rate"))
    fig_roc.add_shape(type="line", line=dict(dash="dash"), x0=0, x1=1, y0=0, y1=1)
    st.plotly_chart(fig_roc, use_container_width=True)

if model_choice == "Random Forest":
    st.markdown("**Feature Importance**")
    importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False).head(10)
    fig_imp = px.bar(importances[::-1], orientation="h", labels={"value": "Importance", "index": "Feature"})
    st.plotly_chart(fig_imp, use_container_width=True)

st.divider()

# ---------- Interactive risk calculator ----------
st.subheader("🔍 Individual Risk Estimator")
st.caption("Enter patient attributes to estimate stroke probability using the model above.")

with st.form("risk_form"):
    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        in_age = st.slider("Age", 0, 100, 50)
        in_gender = st.selectbox("Gender", sorted(df["gender"].unique()))
        in_married = st.selectbox("Ever Married", sorted(df["ever_married"].unique()))
    with cc2:
        in_hyp = st.selectbox("Hypertension", ["No", "Yes"])
        in_heart = st.selectbox("Heart Disease", ["No", "Yes"])
        in_work = st.selectbox("Work Type", sorted(df["work_type"].unique()))
    with cc3:
        in_glucose = st.slider("Avg. Glucose Level", 50.0, 300.0, 100.0)
        in_bmi = st.slider("BMI", 10.0, 60.0, 25.0)
        in_smoke = st.selectbox("Smoking Status", sorted(df["smoking_status"].unique()))
        in_resid = st.selectbox("Residence Type", sorted(df["Residence_type"].unique()))

    submitted = st.form_submit_button("Estimate Risk")

if submitted:
    row = pd.DataFrame([{
        "age": in_age,
        "hypertension": 1 if in_hyp == "Yes" else 0,
        "heart_disease": 1 if in_heart == "Yes" else 0,
        "avg_glucose_level": in_glucose,
        "bmi": in_bmi,
        "gender": in_gender,
        "ever_married": in_married,
        "work_type": in_work,
        "Residence_type": in_resid,
        "smoking_status": in_smoke,
    }])
    row_enc = pd.get_dummies(row, columns=["gender", "ever_married", "work_type", "Residence_type", "smoking_status"])
    row_enc = row_enc.reindex(columns=X.columns, fill_value=0)
    row_scaled = scaler.transform(row_enc)
    proba = model.predict_proba(row_scaled)[0, 1]

    risk_level = "Low" if proba < 0.2 else "Moderate" if proba < 0.5 else "High"
    color = "#4C9F70" if risk_level == "Low" else "#E0A800" if risk_level == "Moderate" else "#D64545"

    st.markdown(
        f"""
        <div style='text-align:center; padding:20px; background-color:{color}22; border-radius:10px;'>
            <h2 style='color:{color};'>Estimated Stroke Probability: {proba*100:.1f}%</h2>
            <h4 style='color:{color};'>Risk Level: {risk_level}</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )
