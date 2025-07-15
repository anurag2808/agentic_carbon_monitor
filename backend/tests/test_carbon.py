from backend.carbon_api import get_carbon_intensity

def test_us_zone():
    result = get_carbon_intensity("US-CAL-CISO")
    assert result["zone"] == "US-CAL-CISO"
    assert result["intensity"] is not None
