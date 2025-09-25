<<<<<<< HEAD
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import date, datetime

# --- Base Schemas ---

class GPSLocation(BaseModel):
    """Represents a GPS coordinate."""
    latitude: float
    longitude: float

# --- User & Auth Schemas ---

class UserBase(BaseModel):
    """Base schema for a user, containing the phone number."""
    phone_number: str = Field(..., pattern=r"^\+[1-9]\d{1,14}$", description="Phone number in E.164 format, e.g., +919876543210")
    name: str = Field(..., min_length=2, description="Full name of the user.")

class UserCreate(UserBase):
    """Schema for creating a new user, includes the password."""
    password: str = Field(..., min_length=8)

class User(UserBase):
    """Schema for returning a user from the API (without the password)."""
    id: int

    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    """Schema for the access token response."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema for the data encoded within the JWT."""
    phone_number: Optional[str] = None

class PasswordResetForm(BaseModel):
    """Schema for the password reset form."""
    token: str
    new_password: str = Field(..., min_length=8)

# --- Farmer Schemas ---

class FarmerInput(BaseModel):
    """Schema for creating a new farmer record."""
    name: str
    phone_number: str = Field(..., pattern=r"^\+[1-9]\d{1,14}$")
    crop: str
    crop_stage: str
    soil_type: str
    language: str
    gps_location: GPSLocation
    enable_sms: bool = True
    enable_whatsapp: bool = False
    enable_voice: bool = False

class Farmer(FarmerInput):
    """Schema for returning a farmer record from the API."""
    id: int
    owner_id: int

    model_config = {
        "from_attributes": True
    }

# --- Advisory Schemas ---

class Weather(BaseModel):
    temp: float
    description: str
    icon: str
    humidity: int

class ForecastDay(BaseModel):
    date: date
    temp_min: float
    temp_max: float
    description: str
    icon: str

class PestPrediction(BaseModel):
    pest: str
    risk: str

class GovtScheme(BaseModel):
    name: str
    description: str
    link: str

class CropHealth(BaseModel):
    status: str
    ndvi: float
    message: str
    message_key: str

class Precaution(BaseModel):
    key: str
    context: Dict[str, Any]

class WaterInfo(BaseModel):
    availability: str
    requirement: str
    recommendation: str

class StructuredAdvisory(BaseModel):
    daily_advice: str
    current_weather: Optional[Weather]
    forecast: List[ForecastDay]
    pest_predictions: List[PestPrediction]
    recommendation: str
    precaution: Precaution
    govt_schemes: List[GovtScheme]
    soil_recommendation: Optional[str] = None
    water_info: Optional[WaterInfo]
    crop_health: Optional[CropHealth] = None

class AdvisoryResponse(BaseModel):
    status: str
    advisory: StructuredAdvisory

class AdvisoryHistoryItem(BaseModel):
    advisory_text: str
    date_sent: datetime
    crop: str

# --- Market Price & Config Schemas ---

class PricePoint(BaseModel):
    date: date
    price: float

class MarketPriceResponse(BaseModel):
    crop: str
    unit: str
    history: List[PricePoint]

class CropInfo(BaseModel):
    stages: List[str]

class AppConfig(BaseModel):
    crops: Dict[str, CropInfo]
    soil_types: List[str]

class APIStatus(BaseModel):
    """Schema for the API status message."""
    message: str
=======
from pydantic import BaseModel, Field, validator
from typing import Literal
from static_data import CROP_DATA, VALID_SOIL_TYPES

class GPSLocation(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class FarmerInput(BaseModel):
    name: str = Field(..., min_length=1)
    phone_number: str = Field(..., pattern=r"^\+[1-9]\d{1,14}$") 
    crop: str = Field(..., min_length=1)
    crop_stage: str = Field(..., min_length=1)
    soil_type: str = Field(..., min_length=1)
    language: Literal["Telugu", "Hindi", "English"]
    gps_location: GPSLocation

    @validator('crop')
    def crop_must_be_in_database(cls, v):
        if v.lower() not in CROP_DATA:
            raise ValueError(f"Crop '{v}' is not supported. Supported crops: {list(CROP_DATA.keys())}")
        return v.lower()

    @validator('crop_stage')
    def crop_stage_must_be_valid_for_crop(cls, v, values, **kwargs):
        crop = values.get('crop')
        if crop and v.lower() not in CROP_DATA[crop]['stages']:
            raise ValueError(f"Invalid stage '{v}' for crop '{crop}'. Valid stages: {list(CROP_DATA[crop]['stages'])}")
        return v.lower()

    @validator('soil_type')
    def soil_type_must_be_valid(cls, v):
        if v.lower() not in VALID_SOIL_TYPES:
            raise ValueError(f"Invalid soil type '{v}'. Allowed types: {list(VALID_SOIL_TYPES)}")
        return v.lower()


class Farmer(FarmerInput):
    id: int

    class Config:
        from_attributes = True  # Updated for Pydantic v2
>>>>>>> 9dcf2d5f559a7a5bb2067331d322a06ab02ddd89
