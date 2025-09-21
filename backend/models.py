from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import JSONB
from backend.database import Base

class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone_number = Column(String, unique=True, index=True)
    language = Column(String)
    crop = Column(String, index=True)
    crop_stage = Column(String)
    soil_type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

class Advisory(Base):
    __tablename__ = "advisories"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, index=True)
    advisory_text = Column(String)
    date_sent = Column(String)
