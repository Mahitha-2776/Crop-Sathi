import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .database import Base, get_db
from .main import app

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """
    Dependency override for tests to use a separate, in-memory database session.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the app's dependency to use the test database for all tests
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def client():
    """
    A fixture that provides a TestClient for making requests to the app.
    It also handles creating and tearing down the database tables for each test function.
    """
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)