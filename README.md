# Stroke Risk Analytics Dashboard

Streamlit dashboard analyzing the Kaggle Stroke Prediction Dataset (5,110 patients),
built for MSBA382 Healthcare Analytics individual project.

## Files
- `Home.py` — landing page with password gate
- `pages/1_Overview.py` — KPIs + sidebar filters
- `pages/2_Demographics.py` — age & gender breakdown
- `pages/3_Risk_Factors.py` — hypertension, heart disease, glucose, BMI, smoking
- `pages/4_Lifestyle_Work.py` — work type, residence, marital status
- `pages/5_Geographic_Burden.py` — WHO DALYs by Country
- `pages/6_Predictive_Model.py` — ML model (Logistic Regression / Random Forest) + interactive risk calculator
- `utils.py` — shared data loading/cleaning
- `data.csv` — the stroke dataset
- `requirements.txt` — Python dependencies

## Password
`stroke2026`

## Notes for the report
- Missing BMI values (201 of 5,110 rows) were imputed with the median.
- Stroke is rare (~4.9% of patients); SMOTE oversampling is used when training the
  predictive model to address class imbalance.
- Residence type (Urban/Rural) is used as the geographic proxy variable since the
  dataset does not include actual location coordinates.
