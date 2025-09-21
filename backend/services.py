import os
import logging
import requests
from datetime import datetime
from sqlalchemy.orm import Session

import backend.models as models, backend.crud as crud
from backend.advisory_config import (
    PEST_DATABASE,
    PESTICIDE_RECOMMENDATIONS,
    GOVT_SCHEMES,
    TRANSLATIONS,
)

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Service Functions ---

def _get_weather_prediction(lat: float, lon: float) -> str:
    """Fetches real weather data from OpenWeatherMap API."""
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"Weather: {weather.capitalize()}, Temp: {temp:.1f}°C."
    except requests.RequestException as e:
        logger.error(f"Weather API request failed: {e}")
        return "Weather data is currently unavailable."

def _get_pest_alerts(crop: str, stage: str) -> str:
    return PEST_DATABASE.get(crop, {}).get(stage, "No specific pest alerts for this stage.")

def _get_pesticide_recommendation(pest_alert: str) -> str:
    return PESTICIDE_RECOMMENDATIONS.get(pest_alert, "Follow local agricultural guidelines for pesticides.")

def _get_precautions(stage: str, weather: str) -> str:
    if "rain" in weather.lower() and stage in ["flowering", "ripening"]:
        return "Precaution: Heavy rain expected. Ensure proper drainage to prevent waterlogging."
    return "Precaution: Monitor crop health daily."

def _get_govt_schemes() -> str:
    return GOVT_SCHEMES["default"]

def _translate(text: str, language: str) -> str:
    if language == "English":
        return text
    # This is a mock translation. In a real app, use a translation API.
    # For production, consider Google Translate API or similar.
    translated_text = text
    for eng, trans in TRANSLATIONS.get(language, {}).items():
        translated_text = translated_text.replace(eng, trans)
    return translated_text

def _send_sms(phone_number: str, message: str):
    print(f"--- SIMULATING SMS to {phone_number} ---")
    # Real implementation with Twilio:
    logger.info(f"Sending SMS to {phone_number}")
    # from twilio.rest import Client
    # account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    # auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    # client = Client(account_sid, auth_token)
    # client.messages.create(
    #     body=message,
    #     from_=os.getenv('TWILIO_PHONE_NUMBER'),
    #     to=phone_number
    # )

def _send_whatsapp(phone_number: str, message: str):
    print(f"--- SIMULATING WhatsApp to {phone_number} ---")
    # Real implementation with Twilio:
    logger.info(f"Sending WhatsApp to {phone_number}")
    # ... similar to SMS but using the WhatsApp 'from_' number
    # from_='whatsapp:' + os.getenv('TWILIO_WHATSAPP_NUMBER'),
    # to='whatsapp:' + phone_number

def _send_voice_alert(phone_number: str, message: str):
    print(f"--- SIMULATING Voice Alert to {phone_number} ---")
    # Real implementation with Twilio:
    logger.info(f"Initiating voice call to {phone_number}")
    # ... use Twilio's TwiML for text-to-speech calls

def generate_and_send_advisory(db: Session, farmer: models.Farmer):
    """Orchestrates the full advisory generation and sending process."""
    
    # 1. Generate advisory components
    weather = _get_weather_prediction(farmer.latitude, farmer.longitude)
    pest_alert = _get_pest_alerts(farmer.crop, farmer.crop_stage)
    pesticide_rec = _get_pesticide_recommendation(pest_alert)
    precautions = _get_precautions(farmer.crop_stage, weather)
    schemes = _get_govt_schemes()

    # 2. Assemble the advisory message
    advisory_parts = [
        f"Hello {farmer.name}, here is your advisory for {farmer.crop}:",
        weather,
        f"Pest Alert: {pest_alert}",
        f"Recommendation: {pesticide_rec}",
        precautions,
        f"Govt. Scheme Info: {schemes}"
    ]
    advisory_message_english = "\n".join(advisory_parts)

    # 3. Translate
    final_message = _translate(advisory_message_english, farmer.language)

    # 4. Send through all channels
    _send_sms(farmer.phone_number, final_message)
    _send_whatsapp(farmer.phone_number, final_message)
    _send_voice_alert(farmer.phone_number, final_message)

    # 5. Log the advisory in the database
    advisory_log = models.Advisory(
        farmer_id=farmer.id,
        advisory_text=final_message,
        date_sent=datetime.utcnow().isoformat()
    )
    db.add(advisory_log)
    db.commit()

    return final_message
