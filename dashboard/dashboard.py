# dashboard/dashboard.py
import streamlit as st
import pandas as pd
import time
import os
import json
# The 'shared' import is no longer needed here, but we keep LIVE_DATABASE for now
# If LIVE_DATABASE also moves to a file, we'll change this.
from backend.shared import LIVE_DATABASE

st.set_page_config(
    page_title="Agentic AI Carbon Dashboard",
    layout="wide"
)

# --- Define path for the shared JSON file in the project root ---
# This correctly finds the root directory from the dashboard folder
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_FILE_PATH = os.path.join(PROJECT_ROOT, "carbon_data.json")


# --- 1. Define the CSS for our custom navigation bar ---
st.markdown("""
    <style>
        /* Main container for the nav links */
        .nav-container {
            display: flex;
            justify-content: flex-end; /* Aligns items to the right */
            gap: 10px; /* Space between nav links */
            padding-top: 1rem;
            padding-bottom: 2rem;
            font-family: 'Source Sans Pro', sans-serif;
            font-size: 16px;
        }
        /* Style for each navigation link */
        .nav-link {
            color: #888; /* Dimmed color for inactive links */
            text-decoration: none; /* Remove underline */
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            transition: background-color 0.3s, color 0.3s;
        }
        /* Style for the currently active page link */
        .nav-link.active {
            color: #FFFFFF; /* White color for the active link */
            background-color: #333; /* Dark background for the active link */
            font-weight: 600;
        }
        /* Hover effect for all links */
        .nav-link:hover {
            color: #FFFFFF;
            text-decoration: none;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. Page Navigation Logic ---
page = st.query_params.get("page", "main")
main_class = "nav-link active" if page == "main" else "nav-link"
nudge_class = "nav-link active" if page == "nudge" else "nav-link"

# --- 3. Build and display the HTML for the navigation bar ---
st.markdown(f"""
    <div class="nav-container">
        <a href="?page=main" target="_self" class="{main_class}">Main Dashboard</a>
        <a href="?page=nudge" target="_self" class="{nudge_class}">Nudging Agent</a>
    </div>
""", unsafe_allow_html=True)


# --- Page 1: Main Dashboard (RESTORED) ---
def render_main_dashboard():
    st.title("🌿 Agentic AI Carbon Monitoring Dashboard")
    st.subheader("AI Jobs Emission Overview")

    try:
        # This pathing is correct because emissions_data.csv is in the same folder
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, "emissions_data.csv")
        data = pd.read_csv(file_path)
        
        st.dataframe(data, use_container_width=True)

        st.subheader("CO₂ Emissions per Job")
        st.bar_chart(data.set_index("job_id")["co2_kg"])

        st.subheader("Optimization Summary")
        optimized_count = data["optimized"].value_counts()
        st.write("✅ Optimized Jobs:", optimized_count.get("Yes", 0))
        st.write("❌ Non-Optimized Jobs:", optimized_count.get("No", 0))
    except FileNotFoundError:
        st.error("Could not find emissions_data.csv. Please make sure the file exists in the 'dashboard' folder.")

# --- Page 2: Nudging Agent Dashboard (STAYS THE SAME) ---
def render_nudging_agent_dashboard():
    st.title("💡 Nudging Agent Live View")
    
    def load_carbon_data():
        """Loads carbon intensity data from the shared JSON file."""
        try:
            with open(JSON_FILE_PATH, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    carbon_intensity_data = load_carbon_data()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("⚡ Top 5 Greenest Regions")
        if carbon_intensity_data:
            df_regions = pd.DataFrame(carbon_intensity_data).head(5)
            df_regions.rename(columns={
                "zone": "Region",
                "intensity": "Intensity (gCO₂/kWh)"
            }, inplace=True)
            st.dataframe(df_regions[['Region', 'Intensity (gCO₂/kWh)']], use_container_width=True, hide_index=True)
        else:
            st.warning("Waiting for agent to fetch carbon data...")

    with col2:
        st.subheader("📊 Live Team Budgets & Status")
        
        intensity_map = {item['zone']: item['intensity'] for item in carbon_intensity_data}
        
        records = []
        for region, teams in LIVE_DATABASE.items():
            for team, data in teams.items():
                remaining = data["budget_gco2"] - data["current_usage_gco2"]
                status = "🚨 WARNING" if remaining < 0 else "✅ OK"
                live_intensity = intensity_map.get(region, "N/A")
                
                records.append({
                    "Region": region,
                    "Live Intensity (gCO₂/kWh)": live_intensity,
                    "Team": team,
                    "Remaining CO₂ (g)": f"{remaining:,.2f}",
                    "Status": status
                })
        
        if records:
            df_budgets = pd.DataFrame(records)
            column_order = ["Region", "Live Intensity (gCO₂/kWh)", "Team", "Remaining CO₂ (g)", "Status"]
            st.dataframe(df_budgets[column_order], use_container_width=True, hide_index=True)
        else:
            st.warning("Waiting for budget data...")

# --- Main Render Logic ---
if page == "main":
    render_main_dashboard()
elif page == "nudge":
    render_nudging_agent_dashboard()
    time.sleep(3)
    st.rerun()
