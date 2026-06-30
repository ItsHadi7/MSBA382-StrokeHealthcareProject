# Stroke Risk Analytics Dashboard

Streamlit dashboard analyzing the Kaggle Stroke Prediction Dataset (5,110 patients),
built for MSBA382 Healthcare Analytics individual project.

## Files
- `Home.py` — landing page with password gate
- `pages/1_Overview.py` — KPIs + sidebar filters
- `pages/2_Demographics.py` — age & gender breakdown
- `pages/3_Risk_Factors.py` — hypertension, heart disease, glucose, BMI, smoking
- `pages/4_Lifestyle_Work.py` — work type, residence, marital status
- `pages/5_Predictive_Model.py` — ML model (Logistic Regression / Random Forest) + interactive risk calculator
- `utils.py` — shared data loading/cleaning
- `data.csv` — the stroke dataset
- `requirements.txt` — Python dependencies

## Default password
`stroke2026` (set in `.streamlit/secrets.toml` locally; set as a Secret on Streamlit Cloud — see below)

## Run locally
```
pip install -r requirements.txt
streamlit run Home.py
```

## Deploy to Streamlit Community Cloud (free, ~5 min)

1. **Push to GitHub**
   - Create a new GitHub repo (e.g. `stroke-dashboard`).
   - Push all files in this folder EXCEPT `.streamlit/secrets.toml` (do not commit secrets — see `.gitignore`).
   ```
   cd stroke-dashboard
   git init
   git add .
   git commit -m "Initial dashboard"
   git branch -M main
   git remote add origin https://github.com/<your-username>/stroke-dashboard.git
   git push -u origin main
   ```

2. **Deploy**
   - Go to https://share.streamlit.io and sign in with GitHub.
   - Click "New app", select your repo, branch `main`, and main file path `Home.py`.
   - Before deploying, click "Advanced settings" → "Secrets" and paste:
     ```
     APP_PASSWORD = "stroke2026"
     ```
   - Click "Deploy". After ~1-2 minutes you'll get a public URL like
     `https://your-app-name.streamlit.app` — this is the link to submit.

3. **Test it**: open the link in an incognito window, confirm the password gate works,
   and click through all 5 pages.

## Notes for the report
- Missing BMI values (201 of 5,110 rows) were imputed with the median.
- Stroke is rare (~4.9% of patients); SMOTE oversampling is used when training the
  predictive model to address class imbalance.
- Residence type (Urban/Rural) is used as the geographic proxy variable since the
  dataset does not include actual location coordinates.
