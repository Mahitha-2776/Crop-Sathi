from backend import services

def test_get_pest_alerts_success():
    """Tests that a valid pest alert is returned for a known crop and stage with no weather data."""
    crop = "rice"
    stage = "vegetative"
    expected_alerts = [
        {"pest": "Stem Borer", "risk": "High"},
        {"pest": "Leaf Folder", "risk": "Medium"}
    ]
    # Pass None for weather to test the base case
    assert services._get_pest_alerts(crop, stage, None, []) == expected_alerts

def test_get_pest_alerts_fallback():
    """Tests that a crop's default alert is returned for an unknown stage with no weather data."""
    crop = "rice"
    stage = "unknown_stage"
    expected_fallback = [
        {"pest": "General Pests", "risk": "Low"}
    ]
    # Pass None for weather to test the fallback case
    assert services._get_pest_alerts(crop, stage, None, []) == expected_fallback

def test_get_pest_alerts_dynamic_risk_rain():
    """Tests that fungal risk is elevated to 'High' during rain."""
    crop = "rice"
    stage = "flowering" # This stage now has "Blast Fungus"
    rainy_weather = {"description": "moderate rain", "temp": 22, "humidity": 90}
    
    alerts = services._get_pest_alerts(crop, stage, rainy_weather, [])
    
    fungus_alert = next((p for p in alerts if "Fungus" in p['pest']), None)
    assert fungus_alert is not None
    assert fungus_alert['risk'] == "High"

def test_get_pest_alerts_dynamic_risk_heat():
    """Tests that Whiteflies risk is elevated to 'High' during high temperatures."""
    hot_weather = {"description": "clear sky", "temp": 30, "humidity": 50}
    alerts = services._get_pest_alerts("cotton", "squaring", hot_weather, [])
    whitefly_alert = next((p for p in alerts if p['pest'] == "Whiteflies"), None)
    assert whitefly_alert['risk'] == "High"

def test_get_pest_alerts_stage_specific_rule():
    """Tests that a stage-specific rule is correctly applied."""
    crop = "cotton"
    stage = "boll-formation" # The stage our new rule targets
    dry_weather = {"description": "clear sky", "temp": 25, "humidity": 50}
    alerts = services._get_pest_alerts(crop, stage, dry_weather, [])
    whitefly_alert = next((p for p in alerts if p['pest'] == "Whitefly"), None)
    assert whitefly_alert is not None
    assert whitefly_alert['risk'] == "High" # Base risk is High, rule adds score to keep it High

def test_get_pest_alerts_forecast_based_rule():
    """Tests that a forecast-based rule correctly increases risk."""
    crop = "rice"
    stage = "flowering" # Has "Blast Fungus" with Medium base risk
    # Weather is currently clear, but rain is coming
    current_weather = {"description": "clear sky", "temp": 25, "humidity": 90}
    forecast_with_rain = [
        {"date": "2024-01-01", "description": "clear sky"},
        {"date": "2024-01-02", "description": "light rain"},
    ]

    alerts = services._get_pest_alerts(crop, stage, current_weather, forecast_with_rain)
    fungus_alert = next((p for p in alerts if "Fungus" in p['pest']), None)
    # Base risk Medium (40) + high humidity (20) + forecast rain (15) = 75, which is High
    assert fungus_alert['risk'] == "High"

def test_get_pesticide_recommendation_highest_risk():
    """Tests that the recommendation is for the pest with the highest risk."""
    predictions = [
        {"pest": "Leaf Folder", "risk": "Medium"},
        {"pest": "Stem Borer", "risk": "High"},
        {"pest": "Gall Midge", "risk": "Low"},
    ]
    assert services._get_pesticide_recommendation(predictions) == "Use Cartap Hydrochloride."

def test_get_pesticide_recommendation_fallback():
    """Tests that a default recommendation is returned for an unknown pest."""
    predictions = [{"pest": "Unknown Pest", "risk": "High"}]
    assert services._get_pesticide_recommendation(predictions) == "Follow local agricultural guidelines for pesticides."

def test_build_translated_message_english():
    """Tests the English message template."""
    data = {
        "name": "Ramesh", "crop": "Rice",
        "current_weather": {"description": "Clear sky", "temp": 28.5},
        "highest_risk_pest": "Stem Borer",
        "recommendation": "Use Cartap Hydrochloride."
    }
    expected_message = (
        "Hello Ramesh, here is your advisory for Rice:\n"
        "Weather: Clear sky, Temp: 28.5°C.\n"
        "Highest Pest Risk: Stem Borer.\n"
        "Recommendation: Use Cartap Hydrochloride."
    )
    assert services._build_translated_message("English", data) == expected_message
