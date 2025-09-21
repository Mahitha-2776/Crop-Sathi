from sqlalchemy.orm import Session
from fastapi import HTTPException
import backend.models as models, backend.schemas as schemas

def get_farmer(db: Session, farmer_id: int):
    return db.query(models.Farmer).filter(models.Farmer.id == farmer_id).first()

def get_farmer_by_phone(db: Session, phone_number: str):
    return db.query(models.Farmer).filter(models.Farmer.phone_number == phone_number).first()

def create_farmer(db: Session, farmer: schemas.FarmerInput):
    existing_farmer = get_farmer_by_phone(db, phone_number=farmer.phone_number)
    if existing_farmer:
        raise HTTPException(status_code=409, detail="A farmer with this phone number already exists.")

    db_farmer = models.Farmer(
        name=farmer.name,
        phone_number=farmer.phone_number,
        language=farmer.language,
        crop=farmer.crop,
        crop_stage=farmer.crop_stage,
        soil_type=farmer.soil_type,
        latitude=farmer.gps_location.latitude,
        longitude=farmer.gps_location.longitude
    )
    db.add(db_farmer)
    db.commit()
    db.refresh(db_farmer)
    return db_farmer
