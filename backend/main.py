from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

import backend.crud as crud, backend.models as models, backend.schemas as schemas, backend.services as services
from backend.database import SessionLocal, engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Crop Sathi API",
    description="Backend for the Crop Sathi crop advisory system.",
    version="1.0.0",
)

@app.post("/farmer-input/", response_model=schemas.Farmer, status_code=201)
def create_farmer_input(farmer: schemas.FarmerInput, db: Session = Depends(get_db)):
    """
    Receives farmer input, validates it, and stores it in the database.
    
    - **name**: Farmer's name
    - **phone_number**: Farmer's phone number in E.164 format (e.g., +919876543210)
    - **crop**: Supported crop (e.g., 'rice', 'wheat')
    - **crop_stage**: A valid stage for the selected crop
    - **soil_type**: A valid soil type
    - **language**: 'English', 'Hindi', or 'Telugu'
    - **gps_location**: Latitude and Longitude
    """
    # The validation is automatically handled by FastAPI using the Pydantic schema.
    # If validation fails, FastAPI returns a 422 error automatically.
    
    db_farmer = crud.create_farmer(db=db, farmer=farmer)
    return db_farmer

@app.get("/advisory/{farmer_id}")
def get_advisory(farmer_id: int, db: Session = Depends(get_db)):
    """
    Generates and sends a crop advisory for a given farmer ID.
    
    This endpoint returns the advisory message directly to the client.
    Notifications (SMS, WhatsApp) are still sent.
    """
    db_farmer = crud.get_farmer(db, farmer_id=farmer_id)
    if db_farmer is None:
        raise HTTPException(status_code=404, detail="Farmer not found")
    
    # We now call the service directly to get the message back.
    # The service itself handles sending notifications.
    advisory_message = services.generate_and_send_advisory(db=db, farmer=db_farmer)
    
    return {"status": "success", "advisory": advisory_message}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Crop Sathi API. Visit /docs for documentation."}
