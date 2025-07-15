import os
import requests
from dotenv import load_dotenv
from pprint import pprint

# Load .env variables
load_dotenv()

API_KEY = os.getenv("ELECTRICITYMAP_API_KEY")
BASE_URL = "https://api.electricitymap.org/v3/carbon-intensity/latest"
DEFAULT_UNIT = "gCO2eq/kWh"

HEADERS = {
    "auth-token": API_KEY
}

# Mock values for zones you don’t have access to
MOCK_ZONES = {
    "EU-DE": 145,
    "IN-DL": 390,
    "SG": 510,
    "FR": 80,
    "GB": 160
}

#Real + Mock zone handler
def get_carbon_intensity(zone: str):
    if zone != "US-CAL-CISO":
        print(f"🔁 Using mock data for zone: {zone}")
        return {
            "zone": zone,
            "intensity": MOCK_ZONES.get(zone, 999),
            "unit": DEFAULT_UNIT
        }

    # Real API call for US-CAL-CISO
    url = f"{BASE_URL}?zone={zone}"
    print(f"\nFetching live data for zone: {zone}")

    try:
        response = requests.get(url, headers=HEADERS)
        print(f"Status code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            intensity = data.get("carbonIntensity")
            unit = data.get("carbonIntensityUnit") or DEFAULT_UNIT

            print(f"Carbon Intensity: {intensity} {unit}")

            return {
                "zone": zone,
                "intensity": intensity,
                "unit": unit
            }
        else:
            print("API Error:", response.text)
            return {"zone": zone, "intensity": None, "error": response.text}
    except Exception as e:
        print("Exception:", e)
        return {"zone": zone, "intensity": None, "error": str(e)}

# Run for all zones
if __name__ == "__main__":
    zones = ["US-CAL-CISO", "EU-DE", "IN-DL", "SG", "FR", "GB"]
    results = []

    for zone in zones:
        result = get_carbon_intensity(zone)
        results.append(result)

    # Sort by lowest intensity
    valid = [r for r in results if r["intensity"] is not None]
    sorted_results = sorted(valid, key=lambda x: x["intensity"])

    print("\nSorted Carbon Intensity by Region:")
    for r in sorted_results:
        print(f"{r['zone']:12} → {r['intensity']} {r['unit']}")
