import streamlit as st
import pandas as pd

st.set_page_config(page_title="Agentic AI Emissions Dashboard", layout="wide")

# Load data
data = pd.read_csv("emissions_data.csv")

st.title("🌿 Agentic AI Carbon Monitoring Dashboard")
st.subheader("AI Jobs Emission Overview")

# Table
st.dataframe(data, use_container_width=True)

# Chart: CO2 per job
st.subheader("CO₂ Emissions per Job")
st.bar_chart(data.set_index("job_id")["co2_kg"])

# Filter by optimization
st.subheader("Optimization Summary")
optimized_count = data["optimized"].value_counts()
st.write("✅ Optimized Jobs:", optimized_count.get("Yes", 0))
st.write("❌ Non-Optimized Jobs:", optimized_count.get("No", 0))















