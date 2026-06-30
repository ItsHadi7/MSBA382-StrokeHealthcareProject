import streamlit as st
import pandas as pd
import plotly.express as px
from utils import require_auth

st.set_page_config(page_title="Geographic Burden", page_icon="🌍", layout="wide")
require_auth()


@st.cache_data
def load_who_data():
    df = pd.read_csv("who_stroke_daly_by_country_2021.csv")
    return df


who_df = load_who_data()

st.title("🌍 Global Stroke Burden")
st.caption(
    "Country-level stroke burden from WHO (2021), measured in DALYs (Disability-Adjusted Life Years) "
    "in thousands. This is a supplementary, population-level dataset — distinct from the individual "
    "patient records used elsewhere in this dashboard — included to address geographic distribution."
)

st.info(
    "ℹ️ **What is a DALY?** One DALY represents one lost year of healthy life, combining years lost to "
    "early death and years lived with disability. Higher values indicate a greater overall stroke burden "
    "on a country's population, not necessarily a higher *rate* per person — larger countries naturally "
    "accumulate more total DALYs."
)

c1, c2, c3 = st.columns(3)
c1.metric("Countries Covered", f"{len(who_df):,}")
c2.metric("Global Total (thousands)", f"{who_df['stroke_daly_thousands'].sum():,.0f}")
c3.metric("Highest Burden", who_df.loc[who_df['stroke_daly_thousands'].idxmax(), 'country'])

st.divider()

st.subheader("Stroke DALYs by Country")
fig = px.choropleth(
    who_df,
    locations="iso3",
    color="stroke_daly_thousands",
    hover_name="country",
    color_continuous_scale="Reds",
    labels={"stroke_daly_thousands": "Stroke DALYs (thousands)"},
)
fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=520,
                   coloraxis_colorbar=dict(title="DALYs (k)"))
st.plotly_chart(fig, use_container_width=True)

st.divider()

col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("Top 15 Countries by Stroke Burden")
    top15 = who_df.sort_values("stroke_daly_thousands", ascending=False).head(15)
    fig2 = px.bar(
        top15.sort_values("stroke_daly_thousands"),
        x="stroke_daly_thousands", y="country", orientation="h",
        color="stroke_daly_thousands", color_continuous_scale="Reds",
        labels={"stroke_daly_thousands": "Stroke DALYs (thousands)", "country": ""},
    )
    fig2.update_layout(coloraxis_showscale=False, height=480)
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("Look Up a Country")
    country_sel = st.selectbox("Select a country", sorted(who_df["country"].unique()))
    row = who_df[who_df["country"] == country_sel].iloc[0]
    rank = int(who_df["stroke_daly_thousands"].rank(ascending=False)[who_df["country"] == country_sel].iloc[0])
    st.metric(f"{country_sel} — Stroke DALYs (thousands)", f"{row['stroke_daly_thousands']:,.1f}")
    st.metric("Global Rank (Burden)", f"#{rank} of {len(who_df)}")

    st.markdown("**Full Country Table**")
    st.dataframe(
        who_df.sort_values("stroke_daly_thousands", ascending=False).reset_index(drop=True),
        use_container_width=True, height=300,
    )

st.markdown(
    "**Insight:** The largest absolute stroke burden is concentrated in the world's most populous "
    "countries (China, India, Indonesia), reflecting population size as much as underlying risk. "
    "For a fairer cross-country comparison, this metric would ideally be normalized by population "
    "(DALYs per 100,000), which is noted as a direction for future work in the consultant manual."
)

st.caption("Source: World Health Organization, Global Health Estimates, 2021.")
