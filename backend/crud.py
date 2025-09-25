from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from . import models, schemas
from .security import get_password_hash, verify_password

def get_user_by_phone_number(db: Session, phone_number: str):
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(phone_number=user.phone_number, name=user.name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_password(db: Session, user: models.User, new_password: str):
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_farmer(db: Session, farmer_id: int):
    return db.query(models.Farmer).filter(models.Farmer.id == farmer_id).first()

def create_farmer(db: Session, farmer_input: schemas.FarmerInput, owner_id: int) -> models.Farmer:
    """
    Creates a new farmer record for an advisory request.
    This allows a user to have multiple farm profiles/advisory requests,
    even with the same phone number.
    """
    db_farmer = models.Farmer(
        name=farmer_input.name,
        phone_number=farmer_input.phone_number,
        crop=farmer_input.crop,
        crop_stage=farmer_input.crop_stage,
        soil_type=farmer_input.soil_type,
        language=farmer_input.language,
        latitude=farmer_input.gps_location.latitude,
        longitude=farmer_input.gps_location.longitude,
        enable_sms=farmer_input.enable_sms,
        enable_whatsapp=farmer_input.enable_whatsapp,
        enable_voice=farmer_input.enable_voice,
        owner_id=owner_id,
    )
    db.add(db_farmer)
    db.commit()
    db.refresh(db_farmer)
    return db_farmer

def get_advisories_by_owner_id(db: Session, owner_id: int) -> List[schemas.AdvisoryHistoryItem]:
    """
    Retrieves all advisories for a given owner, joining with the farmer to get crop info.
    Orders by the most recent advisory first.
    """
    advisories_with_crop = db.query(models.Advisory, models.Farmer.crop)\
        .join(models.Farmer, models.Advisory.farmer_id == models.Farmer.id)\
        .filter(models.Farmer.owner_id == owner_id)\
        .order_by(models.Advisory.date_sent.desc())\
        .all()
    
    return [
        schemas.AdvisoryHistoryItem(
            advisory_text=advisory.advisory_text,
            date_sent=advisory.date_sent,
            crop=crop.capitalize()
        ) for advisory, crop in advisories_with_crop
    ]
