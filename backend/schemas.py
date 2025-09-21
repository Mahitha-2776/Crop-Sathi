from pydantic import BaseModel, Field, validator
from typing import Literal

from backend.static_data import CROP_DATA, VALID_SOIL_TYPES

class GPSLocation(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class FarmerInput(BaseModel):
    name: str = Field(..., min_length=1)
    # A dummy phone number for demonstration
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
        orm_mode = True
