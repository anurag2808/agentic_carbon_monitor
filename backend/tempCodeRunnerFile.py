if __name__ == "__main__":
#     zones = ["US-CAL-CISO", "EU-DE", "IN-DL", "SG", "FR", "GB"]  # France, Germany, India (Delhi), Singapore, UK
#     results = []

#     for zone in zones:
#         result = get_carbon_intensity(zone)
#         results.append(result)

#     # Filter valid responses
#     valid_results = [r for r in results if r.get("intensity") is not None]
#     sorted_results = sorted(valid_results, key=lambda x: x["intensity"])

#     print("\n✅ Sorted Carbon Intensity by Region:")
#     for r in sorted_results:
#         print(f"{r['zone']:12} → {r['intensity']} {r['unit']}")