import os
from sqlalchemy import create_engine
<<<<<<< HEAD
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Check for a production DATABASE_URL, otherwise fall back to local SQLite.
# This URL will be provided by your cloud hosting service.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cropsathi.db")

# Adjust engine creation for PostgreSQL vs SQLite
if DATABASE_URL.startswith("postgres"):
    engine = create_engine(DATABASE_URL)
else:
    # SQLite requires a specific connect_args setting.
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )

=======
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
>>>>>>> 9dcf2d5f559a7a5bb2067331d322a06ab02ddd89
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

<<<<<<< HEAD
# --- Dependency to get DB session ---
=======
# Dependency to get DB session
>>>>>>> 9dcf2d5f559a7a5bb2067331d322a06ab02ddd89
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
<<<<<<< HEAD

def create_db_and_tables():
    """Creates all database tables."""
    Base.metadata.create_all(bind=engine)
=======
>>>>>>> 9dcf2d5f559a7a5bb2067331d322a06ab02ddd89
