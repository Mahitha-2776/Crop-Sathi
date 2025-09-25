import os
from datetime import timedelta, datetime
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import List
from sqlalchemy.orm import Session
from . import crud, schemas, services, models, auth
from .database import SessionLocal, engine, get_db, create_db_and_tables
from .static_data import CROP_DATA, VALID_SOIL_TYPES, MARKET_PRICES

# Load environment variables from .env file
load_dotenv()

# --- Path Configuration for Serving Frontend ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")

def startup_event():
    """Function to run on application startup."""
    create_db_and_tables()
    print("✅ Database tables created.")

# --- Rate Limiting Setup ---
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Crop Sathi API",
    description="Backend for the Crop Sathi crop advisory system.",
    version="1.0.0",
    servers=[
        {"url": "http://127.0.0.1:8000", "description": "Local development server"},
        {"url": "https://cropsathi.example.com", "description": "Production server (placeholder)"},
    ]
)
app.add_event_handler("startup", startup_event)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Load allowed origins from environment, with a sensible default for local development
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",")

app.add_middleware(
    CORSMiddleware,
    # Allow specific origins for local development, including the separate frontend server port.
    # In production, this should be set to the domain of your frontend application.
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Reusable Dependencies ---

def validate_input_dependency(farmer_input: schemas.FarmerInput):
    """A dependency that validates farmer input before the endpoint logic runs."""
    services.validate_farmer_input(farmer_input)
    return farmer_input

@app.post("/token", response_model=schemas.Token)
@limiter.limit("10/minute")
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, phone_number=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.phone_number}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone_number(db, phone_number=user.phone_number)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return crud.create_user(db=db, user=user)

@app.post("/password-recovery/{phone_number}", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
def recover_password(request: Request, phone_number: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Initiates the password recovery process for a user.
    """
    # The service function handles the logic of checking if the user exists
    # and scheduling the notification.
    services.initiate_password_recovery(db, phone_number, background_tasks)
    # Always return a success message to prevent user enumeration
    return {"msg": "If an account with that phone number exists, a password recovery message has been sent."}

@app.post("/reset-password/", status_code=status.HTTP_200_OK)
def reset_password(form_data: schemas.PasswordResetForm, db: Session = Depends(get_db)):
    phone_number = auth.verify_password_reset_token(form_data.token)
    if not phone_number:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    user = crud.get_user_by_phone_number(db, phone_number=phone_number)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    crud.update_user_password(db=db, user=user, new_password=form_data.new_password)
    return {"msg": "Password updated successfully"}

@app.post("/advisory/", response_model=schemas.AdvisoryResponse)
def get_or_create_advisory(background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user), farmer_input: schemas.FarmerInput = Depends(validate_input_dependency)):
    """
    Generates and sends a crop advisory. If a farmer with the phone number
    doesn't exist, it creates one. Otherwise, it uses the existing farmer.
    
    This endpoint immediately returns a preview of the advisory message.
    The actual sending of notifications (SMS, WhatsApp) and logging to the
    database are handled as background tasks to ensure a fast response.
    """
    # Use a "get or create" pattern for the farmer
    db_farmer = crud.create_farmer(db=db, farmer_input=farmer_input, owner_id=current_user.id)
    
    # Generate structured advisory data for the API response.
    advisory_data = services.generate_advisory_data(farmer=db_farmer)
    
    # Schedule the slow tasks (DB logging, sending notifications) to run in the background.
    background_tasks.add_task(
        services.send_and_log_advisory, farmer_id=db_farmer.id, message_to_send=advisory_data["full_text"]
    )
    
    return {
        "status": "Advisory generation started", 
        "advisory": advisory_data['structured']
    }

@app.get("/advisories/history", response_model=List[schemas.AdvisoryHistoryItem])
def get_advisory_history(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    """
    Returns a list of all past advisories for the currently logged-in user.
    """
    # The CRUD function now returns the data in the correct response shape.
    return crud.get_advisories_by_owner_id(db, owner_id=current_user.id)

@app.get("/market-price/{crop}", response_model=schemas.MarketPriceResponse, dependencies=[Depends(auth.get_current_active_user)])
def get_market_price(crop: str):
    """
    Returns simulated market price data for a given crop.
    """
    price_data = MARKET_PRICES.get(crop.lower())
    if not price_data:
        raise HTTPException(status_code=404, detail=f"Market price data not found for crop '{crop}'.")
    return {"crop": crop, **price_data}

@app.get("/config", response_model=schemas.AppConfig)
def get_app_config():
    """
    Returns the application configuration including supported crops and soil types.
    """
    return {
        "crops": CROP_DATA,
        "soil_types": sorted(list(VALID_SOIL_TYPES))
    }

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user

@app.get("/api-status", response_model=schemas.APIStatus)
def get_api_status():
    """Returns a simple status message for the API."""
    return {"message": "Welcome to the Crop Sathi API. Visit /docs for documentation."}

# --- Serve Frontend ---
# This must be the last route, as it's a catch-all for serving the frontend.
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static-frontend")
