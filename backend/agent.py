from carbon_api import get_carbon_intensity

zones = ["US-CAL-CISO", "EU-DE", "IN-DL", "SG"]
results = []

for zone in zones:
    result = get_carbon_intensity(zone)
    results.append(result)

# Sort by lowest carbon intensity
sorted_results = sorted([r for r in results if r["intensity"] is not None], key=lambda x: x["intensity"])

print("Carbon intensity by region:")
for r in sorted_results:
    print(f"{r['zone']}: {r['intensity']} {r['unit']}")
