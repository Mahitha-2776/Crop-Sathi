import os
import logging
import requests
from fastapi import BackgroundTasks
from fastapi import HTTPException, status
from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioRestException
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Any, Optional, Tuple
from . import auth
from . import models, crud
from .static_data import (
    PEST_DATABASE,
    PESTICIDE_RECOMMENDATIONS,
    GOVT_SCHEMES,
    MESSAGE_TEMPLATES,
    CROP_DATA,
    SOIL_RECOMMENDATIONS,
    VALID_SOIL_TYPES,
)

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Twilio Client Initialization ---
# Centralize credential loading and client instantiation for efficiency.
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

twilio_client = None
if all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN]):
    try:
        # The client is initialized once and reused across functions.
        twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        logger.info("Twilio client initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Twilio client: {e}")
else:
    # This warning will now appear once on startup, which is cleaner.
    logger.warning("Twilio credentials not fully configured. SMS/WhatsApp/Voice will be simulated in console.")

# --- Constants ---
RISK_LEVEL_SCORES = {"Low": 1, "Medium": 2, "High": 3}

# --- Service Functions ---

def validate_farmer_input(farmer_input):
    """
    Validates crop, crop_stage, and soil_type against static data.
    Raises HTTPException if validation fails.
    """
    crop = farmer_input.crop.lower()
    stage = farmer_input.crop_stage.lower()
    soil = farmer_input.soil_type.lower()

    if crop not in CROP_DATA:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid crop '{farmer_input.crop}'.")
    if stage not in CROP_DATA[crop]['stages']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid stage '{farmer_input.crop_stage}' for crop '{farmer_input.crop}'.")
    if soil not in VALID_SOIL_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid soil type '{farmer_input.soil_type}'.")


def _get_weather_data(lat: float, lon: float) -> dict:
    """Fetches current weather and 5-day forecast from OpenWeatherMap."""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        logger.error("WEATHER_API_KEY not set.")
        return {"current": None, "forecast": []}

    # Using the 5-day/3-hour forecast endpoint which is available on the free tier
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"

    timeout_seconds = int(os.getenv("WEATHER_API_TIMEOUT", "5"))
    
    try:
        response = requests.get(url, timeout=timeout_seconds)
        response.raise_for_status()
        data = response.json()

        # Current weather can be approximated by the first item in the forecast
        current_data = data['list'][0]
        current_weather = {
            "temp": current_data['main']['temp'],
            "description": current_data['weather'][0]['description'].capitalize(),
            "icon": current_data['weather'][0]['icon'],
            "humidity": current_data['main']['humidity']
        }

        # Process the list to get a daily forecast
        daily_forecasts = {}
        for forecast in data['list']:
            date = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d')
            if date not in daily_forecasts:
                daily_forecasts[date] = {"temps": [], "icons": {}, "descriptions": {}}
            
            daily_forecasts[date]["temps"].append(forecast['main']['temp'])
            icon = forecast['weather'][0]['icon']
            daily_forecasts[date]["icons"][icon] = daily_forecasts[date]["icons"].get(icon, 0) + 1
            desc = forecast['weather'][0]['description'].capitalize()
            daily_forecasts[date]["descriptions"][desc] = daily_forecasts[date]["descriptions"].get(desc, 0) + 1

        processed_forecast = []
        # Iterate through sorted dates and take the first 5 days of forecast
        for date, values in sorted(daily_forecasts.items())[:5]:
            processed_forecast.append({
                "date": date,
                "temp_min": min(values['temps']),
                "temp_max": max(values['temps']),
                "description": max(values['descriptions'], key=values['descriptions'].get),
                "icon": max(values['icons'], key=values['icons'].get)
            })

        return {"current": current_weather, "forecast": processed_forecast}
    except requests.RequestException as e:
        logger.error(f"Weather API request failed: {e}")
        return {"current": None, "forecast": []}

# --- Pest Prediction Rules Engine ---

BASE_RISK_SCORES = {"Low": 10, "Medium": 40, "High": 70}

def _score_to_risk_level(score: int) -> str:
    if score >= 70: return "High"
    if score >= 40: return "Medium"
    return "Low"

def _fungal_risk_rule(pest: dict, weather: dict, stage: str, forecast: list) -> int:
    """Fungal risks increase significantly with high humidity and rain."""
    score_adjustment = 0
    if "fungus" in pest['pest'].lower() or "blight" in pest['pest'].lower():
        if "rain" in weather.get("description", "").lower():
            score_adjustment += 40 # Major factor
        if weather.get("humidity", 50) > 85:
            score_adjustment += 20 # Minor factor
    return score_adjustment

def _heat_loving_pest_rule(pest: dict, weather: dict, stage: str, forecast: list) -> int:
    """Pests like mites and whiteflies thrive in heat."""
    if pest['pest'] in ["Spider Mites", "Whiteflies", "Whitefly"] and weather.get("temp", 15) > 28:
        return 30
    return 0

def _aphid_risk_rule(pest: dict, weather: dict, stage: str, forecast: list) -> int:
    """Aphids prefer moderate, non-extreme temperatures."""
    if pest['pest'] == "Aphid":
        temp = weather.get("temp", 15)
        if 18 <= temp <= 25:
            return 20 # Ideal conditions
        elif temp > 30:
            return -10 # Too hot, risk decreases
    return 0

def _whitefly_boll_formation_rule(pest: dict, weather: dict, stage: str, forecast: list) -> int:
    """STAGE-SPECIFIC RULE: Whitefly risk is highest during boll formation, especially in dry conditions."""
    if pest['pest'] == "Whitefly" and stage == "boll-formation":
        if weather.get("humidity", 70) < 60:
            # Add a significant score boost for this critical combination
            return 25
    return 0

def _forecast_rain_fungal_rule(pest: dict, weather: dict, stage: str, forecast: list) -> int:
    """FORECAST-BASED RULE: Proactively increase fungal risk if rain is forecast in the next 3 days."""
    if "fungus" in pest['pest'].lower() or "blight" in pest['pest'].lower():
        # Check the next 3 days in the forecast
        for day in forecast[:3]:
            if "rain" in day.get("description", "").lower():
                # Add a moderate score boost for proactive alerts
                return 15
    return 0

_PEST_RISK_RULES = [
    _fungal_risk_rule, _heat_loving_pest_rule, _aphid_risk_rule,
    _whitefly_boll_formation_rule, _forecast_rain_fungal_rule
]

# --- Main Service Functions ---

def _get_pest_alerts(crop: str, stage: str, current_weather: Optional[dict], weather_forecast: list) -> list[dict]:
    """
    Gets pest alerts and dynamically adjusts risk based on a more sophisticated
    rules engine and scoring system.
    """
    crop_pests = PEST_DATABASE.get(crop.lower(), PEST_DATABASE.get("default", {}))
    base_predictions = crop_pests.get(stage.lower(), crop_pests.get("default", []))

    if not current_weather:
        return [p.copy() for p in base_predictions] # Return default risks if no weather data

    # Apply rules and calculate new risk levels
    dynamic_predictions = []
    for pest_prediction in base_predictions:
        pest = pest_prediction.copy()
        current_score = BASE_RISK_SCORES.get(pest['risk'], 10)
        for rule in _PEST_RISK_RULES:
            current_score += rule(pest, current_weather, stage, weather_forecast)
        current_score = max(0, min(100, current_score)) # Bound score between 0-100
        pest['risk'] = _score_to_risk_level(current_score)
        dynamic_predictions.append(pest)

    return dynamic_predictions

def _get_pesticide_recommendation(pest_predictions: list[dict]) -> Tuple[str, Optional[str]]:
    """Recommend based on the highest risk pest. Returns recommendation and pest name."""
    if not pest_predictions:
        return PESTICIDE_RECOMMENDATIONS["Default"], None
    
    highest_risk_pest = max(pest_predictions, key=lambda p: RISK_LEVEL_SCORES.get(p.get('risk'), 0))
    recommendation = PESTICIDE_RECOMMENDATIONS.get(highest_risk_pest['pest'], PESTICIDE_RECOMMENDATIONS["Default"])
    return recommendation, highest_risk_pest['pest']


def _get_precautions(stage: str, weather: str) -> dict:
    """Returns a dictionary with a translation key and context for a precaution."""
    if weather and "rain" in weather.lower() and stage in ["flowering", "ripening"]:
        return {"key": "precaution_rain", "context": {}}
    # The default precaution
    return {"key": "precaution_default", "context": {}}


def _get_govt_schemes(crop: str) -> list[dict]:
    return GOVT_SCHEMES.get(crop.lower(), GOVT_SCHEMES["default"])

def _get_satellite_data(lat: float, lon: float) -> Optional[dict]:
    """
    Simulates fetching satellite data (like NDVI) for a given coordinate.
    In a real application, this would call a service like Sentinel Hub.
    """
    # To make this real, you would:
    # 1. Sign up for a free account at Sentinel Hub (https://www.sentinel-hub.com/).
    # 2. Get your 'instance ID' and store it as an environment variable.
    # 3. Use a library like 'sentinelhub-py' to make the request.
    #
    # The request would define a bounding box around the lat/lon, specify the
    # date range, and use a script to calculate NDVI from Sentinel-2 bands.
    #
    # Example Bounding Box (approx. 100x100 meters for a small farm):
    # bbox_size = 0.001  # Roughly 100 meters
    # bbox = [lon - bbox_size, lat - bbox_size, lon + bbox_size, lat + bbox_size]

    # --- SIMULATION ---
    # We'll simulate the result for demonstration purposes.
    # A random NDVI value is generated to show different health statuses.
    import random
    simulated_ndvi = random.uniform(0.2, 0.85)
    logger.info(f"Simulated satellite data fetch. NDVI: {simulated_ndvi:.2f}")

    return {"ndvi": simulated_ndvi}

def _get_water_info(crop: str, forecast: list) -> Optional[dict]:
    """Simulates water availability and provides crop water requirements."""
    # 1. Simulate local water availability based on forecast
    rain_in_forecast = any("rain" in day.get("description", "").lower() for day in forecast)
    
    # 2. Get crop-specific water requirement
    crop_info = CROP_DATA.get(crop.lower(), {})
    requirement_mm = crop_info.get("water_requirement_mm")
    if not requirement_mm:
        return None
    
    return {
        "availability_key": "water_availability_good" if rain_in_forecast else "water_availability_moderate",
        "requirement_mm": requirement_mm,
        "recommendation_detail_key": "water_detail_rain" if rain_in_forecast else "water_detail_no_rain",
    }

def _interpret_ndvi(ndvi: float) -> dict:
    """
    Translates an NDVI value into a human-readable status and message.
    NDVI ranges from -1 to +1. For vegetation, it's typically 0.2 to 0.9.
    """
    if ndvi > 0.65:
        return {
            "status": "Healthy",
            "ndvi": ndvi,
            "message": "Crop vegetation appears dense and healthy. Continue standard practices.",
            "message_key": "crop_health_healthy"
        }
    elif ndvi > 0.4:
        return {
            "status": "Moderate",
            "ndvi": ndvi,
            "message": "Crop vegetation is moderate. Monitor for signs of uneven growth or nutrient deficiency.",
            "message_key": "crop_health_moderate"
        }
    else:
        return {
            "status": "Stressed",
            "ndvi": ndvi,
            "message": "Low vegetation detected. This could indicate stress from lack of water, nutrients, or pests. A field inspection is highly recommended.",
            "message_key": "crop_health_stressed"
        }

def _build_translated_message(language: str, data: dict) -> str:
    """Builds a translated advisory message using templates."""
    templates = MESSAGE_TEMPLATES.get(language, MESSAGE_TEMPLATES["English"])
    
    message_parts = []
    
    # 1. Greeting
    message_parts.append(templates["greeting"].format(name=data["name"], crop=data["crop"]))
    
    # 2. Weather
    current_weather = data.get("current_weather")
    if current_weather:
        message_parts.append(templates["weather"].format(
            description=current_weather["description"],
            temp=f"{current_weather['temp']:.1f}"
        ))
    else:
        message_parts.append(templates["weather_unavailable"])
        
    # 3. Pest Risk
    if data.get("highest_risk_pest"):
        message_parts.append(templates["pest_risk"].format(pest=data["highest_risk_pest"]))
    else:
        message_parts.append(templates["no_pest_risk"])
        
    # 4. Recommendation
    if data.get("recommendation"):
        message_parts.append(templates["recommendation"].format(recommendation=data["recommendation"]))

    # 5. Crop Health
    if data.get("crop_health"):
        health_info = data["crop_health"]
        template_key = health_info["message_key"]
        if template_key in templates:
            message_parts.append(templates[template_key].format(ndvi=health_info["ndvi"]))
        
    return "\n".join(message_parts)

def _send_sms(phone_number: str, message: str):
    """Sends an SMS using Twilio, with a fallback to console for development."""
    if not twilio_client or not TWILIO_PHONE_NUMBER:
        logger.warning("Simulating SMS to console because Twilio is not fully configured.")
        print(f"--- DEV-MODE SMS to {phone_number} ---\n{message}\n---------------------------------")
        return

    try:
        message_instance = twilio_client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        logger.info(f"SMS sent to {phone_number} successfully. SID: {message_instance.sid}")
    except TwilioRestException as e:
        logger.error(f"Failed to send SMS to {phone_number} via Twilio. Error: {e}")

def _send_whatsapp(phone_number: str, message: str):
    """Sends a WhatsApp message using Twilio, with a fallback to console."""
    if not twilio_client or not TWILIO_WHATSAPP_NUMBER:
        logger.warning("Simulating WhatsApp to console because Twilio is not fully configured.")
        print(f"--- DEV-MODE WhatsApp to {phone_number} ---\n{message}\n---------------------------------")
        return

    try:
        message_instance = twilio_client.messages.create(
            body=message,
            from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',
            to=f'whatsapp:{phone_number}'
        )
        logger.info(f"WhatsApp message sent to {phone_number} successfully. SID: {message_instance.sid}")
    except TwilioRestException as e:
        logger.error(f"Failed to send WhatsApp to {phone_number} via Twilio. Error: {e}")

def _send_voice_alert(phone_number: str, message: str):
    """Initiates a text-to-speech voice call using Twilio."""
    if not twilio_client or not TWILIO_PHONE_NUMBER:
        logger.warning("Simulating Voice Call to console because Twilio is not fully configured.")
        print(f"--- DEV-MODE Voice Call to {phone_number} ---\nSpoken message: {message}\n---------------------------------")
        return

    # TwiML for a simple text-to-speech message. We use en-IN for Indian English.
    twiml = f'<Response><Say language="en-IN">{message}</Say></Response>'

    try:
        call_instance = twilio_client.calls.create(
            twiml=twiml,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        logger.info(f"Voice call initiated to {phone_number} successfully. SID: {call_instance.sid}")
    except TwilioRestException as e:
        logger.error(f"Failed to initiate voice call to {phone_number} via Twilio. Error: {e}")

def send_password_reset_notification(phone_number: str, token: str):
    """
    Sends a multi-language password reset notification via SMS to ensure it's understood by the user.
    """
    # Use a relative URL for the reset link. This makes it environment-agnostic.
    # The user will click this link from their browser, which will be pointed at the correct server (e.g., localhost:8000).
    # The full URL will be constructed by the user's browser.
    reset_url = f"/?token={token}#reset-password"
    
    messages = []
    for lang in ["English", "Hindi", "Telugu"]:
        template = MESSAGE_TEMPLATES[lang].get("password_reset", "Your Crop Sathi password reset link is: {reset_url}")
        messages.append(template.format(reset_url=reset_url))
        
    full_message = "\n---\n".join(messages)
    _send_sms(phone_number=phone_number, message=full_message)

def initiate_password_recovery(db: Session, phone_number: str, background_tasks: BackgroundTasks):
    """
    If a user exists for the given phone number, create a password reset token
    and schedule a notification to be sent.
    """
    user = crud.get_user_by_phone_number(db, phone_number=phone_number)
    if user:
        password_reset_token = auth.create_password_reset_token(phone_number=phone_number)
        background_tasks.add_task(
            send_password_reset_notification, phone_number=user.phone_number, token=password_reset_token
        )

def generate_advisory_data(farmer: models.Farmer) -> dict:
    """Generates structured advisory data and a full text version."""
    # 1. Get required data
    weather_data = _get_weather_data(farmer.latitude, farmer.longitude)
    current_weather = weather_data.get("current")
    weather_forecast = weather_data.get("forecast")
    pest_predictions = _get_pest_alerts(farmer.crop, farmer.crop_stage, current_weather, weather_forecast)
    pesticide_rec, highest_risk_pest_name = _get_pesticide_recommendation(pest_predictions)
    
    # Get the structured precaution data (key and context)
    precaution_data = _get_precautions(
        farmer.crop_stage, current_weather['description'] if current_weather else ""
    )
    water_info = _get_water_info(farmer.crop, weather_forecast)
    schemes = _get_govt_schemes(farmer.crop)
    
    # 2. Get satellite-based crop health
    crop_health_info = None
    satellite_data = _get_satellite_data(farmer.latitude, farmer.longitude)
    if satellite_data and 'ndvi' in satellite_data:
        crop_health_info = _interpret_ndvi(satellite_data['ndvi'])

    # 3. Get templates for the farmer's language
    templates = MESSAGE_TEMPLATES.get(farmer.language, MESSAGE_TEMPLATES["English"])

    # 4. Assemble translated structured data for the dashboard
    # Translate precaution text
    precaution_text = templates.get(precaution_data['key'], "Monitor crop health.")
    soil_recommendation_text = SOIL_RECOMMENDATIONS.get(farmer.soil_type.lower(), SOIL_RECOMMENDATIONS["default"])

    # Translate daily advice
    daily_advice = ""
    if current_weather:
        daily_advice = templates.get("daily_advice", "").format(
            description=current_weather['description'],
            temp=f"{current_weather['temp']:.1f}",
            humidity=current_weather['humidity'],
            precaution_text=precaution_text
        )

    # Translate water info
    translated_water_info = None
    if water_info:
        translated_water_info = {
            "availability": templates.get(water_info['availability_key'], ""),
            "requirement": templates.get("water_requirement", "").format(value=water_info['requirement_mm']),
            "recommendation": templates.get("water_recommendation", "").format(
                detail=templates.get(water_info['recommendation_detail_key'], "")
            )
        }

    structured_advisory_data = {
        "daily_advice": daily_advice,
        "current_weather": current_weather,
        "forecast": weather_forecast,
        "pest_predictions": pest_predictions,
        "recommendation": templates.get("recommendation", "").format(recommendation=pesticide_rec),
        "precaution": precaution_data,  # Send the structured data instead of pre-formatted text
        "govt_schemes": schemes,
        "soil_recommendation": soil_recommendation_text,
        "water_info": translated_water_info,
        "crop_health": crop_health_info,
    }
    
    # 5. Assemble data for the text/voice message builder
    translation_data = {
        "name": farmer.name,
        "crop": farmer.crop,
        "current_weather": current_weather,
        "highest_risk_pest": highest_risk_pest_name,
        "recommendation": pesticide_rec,
        "crop_health": crop_health_info,
    }

    # 6. Build the final translated message for notifications
    full_text_message = _build_translated_message(farmer.language, translation_data)

    return {"structured": structured_advisory_data, "full_text": full_text_message}

def send_and_log_advisory(farmer_id: int, message_to_send: str):
    """
    Sends the advisory through all channels and logs it to the database.
    Designed to be run as a background task. It creates its own DB session.
    """
    from .database import SessionLocal # Import here to avoid potential circular dependencies

    db = SessionLocal()
    try:
        farmer = crud.get_farmer(db, farmer_id=farmer_id)
        if not farmer:
            logger.error(f"Background task failed: Farmer with ID {farmer_id} not found.")
            return

        # 1. Send through all channels
        if farmer.enable_sms:
            _send_sms(farmer.phone_number, message_to_send)
        if farmer.enable_whatsapp:
            _send_whatsapp(farmer.phone_number, message_to_send)
        if farmer.enable_voice:
            _send_voice_alert(farmer.phone_number, message_to_send)

        # 2. Log the advisory in the database
        db_advisory = models.Advisory(farmer_id=farmer.id, advisory_text=message_to_send)
        db.add(db_advisory)
        db.commit()
        logger.info(f"Advisory for farmer {farmer.id} sent and logged successfully.")
    finally:
        db.close()
