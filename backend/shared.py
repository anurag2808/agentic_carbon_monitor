from collections import deque

LIVE_DATABASE = {
    "ml-team": {"budget_gco2": 2000, "current_usage_gco2": 0},
    "data-eng": {"budget_gco2": 3500, "current_usage_gco2": 0},
    "research": {"budget_gco2": 1500, "current_usage_gco2": 0},
}

JOB_QUEUE = deque()
