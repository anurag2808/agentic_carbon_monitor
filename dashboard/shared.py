# shared.py
from collections import deque

# 1. LIVE_DATABASE is now nested by region to support region-specific budgets.
LIVE_DATABASE = {
    "US-CAL-CISO": {
        "ml-team": {"budget_gco2": 2000, "current_usage_gco2": 0},
        "data-eng": {"budget_gco2": 3500, "current_usage_gco2": 0},
    },
    "EU-DE": {
        "ml-team": {"budget_gco2": 1800, "current_usage_gco2": 0},
        "research": {"budget_gco2": 1500, "current_usage_gco2": 0},
    },
    "IN-DL": {
         "data-eng": {"budget_gco2": 3000, "current_usage_gco2": 0},
         "research": {"budget_gco2": 1200, "current_usage_gco2": 0},
    }
}

# 2. JOB_QUEUE remains the same.
JOB_QUEUE = deque()

# 3. New shared list for the dashboard to read live carbon intensity data.
CARBON_INTENSITY_DATA = []