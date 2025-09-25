from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    farmers = relationship("Farmer", back_populates="owner")

class Farmer(Base):
    __tablename__ = "farmers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    phone_number = Column(String, index=True)
    crop = Column(String)
    crop_stage = Column(String)
    soil_type = Column(String)
    language = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    
    enable_sms = Column(Boolean, default=True)
    enable_whatsapp = Column(Boolean, default=False)
    enable_voice = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="farmers")
    advisories = relationship("Advisory", back_populates="farmer")

class Advisory(Base):
    __tablename__ = "advisories"
    id = Column(Integer, primary_key=True, index=True)
    advisory_text = Column(String)
    date_sent = Column(DateTime, default=datetime.utcnow)
    
    farmer_id = Column(Integer, ForeignKey("farmers.id"))
    farmer = relationship("Farmer", back_populates="advisories")
