import streamlit as st
import pandas as pd
from datetime import datetime, date
from notion_utils import fetch_jobs
from analysis_agent import analyze_patterns

st.set_page_config(page_title="Career Agent", layout="wide")

st.title("Autonomous Career Optimization Agent")

jobs = fetch_jobs()

if not jobs:
    st.warning("No applications found.")
    st.stop()

df = pd.DataFrame(jobs)

# ---- KPIs ----
total_apps = len(df)
applied = len(df[df["status"] == "Applied"])
interviews = len(df[df["status"] == "Interview"])
offers = len(df[df["status"] == "Offer"])
rejected = len(df[df["status"] == "Rejected"])

conversion = round(((interviews + offers) / total_apps) * 100, 2) if total_apps else 0

st.write("## Summary Metrics")
st.write(f"Total Applications: {total_apps}")
st.write(f"Applied: {applied}")
st.write(f"Interviews: {interviews}")
st.write(f"Offers: {offers}")
st.write(f"Rejected: {rejected}")
st.write(f"Conversion Rate: {conversion}%")

st.write("---")

# ---- AI INSIGHTS ----
st.write("## AI Strategic Insights")

insights = analyze_patterns(jobs)

if insights:
    st.write(insights)
else:
    st.write("No insights generated.")

st.write("---")

# ---- TABLE ----
st.write("## Applications Overview")
st.dataframe(df)