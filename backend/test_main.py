from fastapi.testclient import TestClient

# Note: We don't need to import 'client' from conftest, pytest finds it automatically.


def test_read_api_status(client: TestClient):
    """Tests the public API status endpoint."""
    response = client.get("/api-status")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Crop Sathi API. Visit /docs for documentation."
    }


def test_get_app_config(client: TestClient):
    """Tests that the app configuration is loaded and returned correctly."""
    response = client.get("/config")
    assert response.status_code == 200
    data = response.json()
    assert "crops" in data
    assert "rice" in data["crops"]
    assert "soil_types" in data
    assert "alluvial" in data["soil_types"]


def test_read_users_me_unauthorized(client: TestClient):
    """Tests that a protected endpoint requires authentication."""
    response = client.get("/users/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_full_auth_flow_and_advisory(client: TestClient):
    """Tests the full user flow: register, login, and request an advisory."""
    # 1. Register a new user
    register_response = client.post(
        "/users/",
        json={"name": "Test User", "phone_number": "+919999988888", "password": "testpassword123"},
    )
    assert register_response.status_code == 201
    user_data = register_response.json()
    assert user_data["phone_number"] == "+919999988888"
    assert user_data["name"] == "Test User"

    # 2. Log in to get a token
    login_response = client.post(
        "/token",
        data={"username": "+919999988888", "password": "testpassword123"},
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    token = token_data["access_token"]

    # 3. Use the token to get an advisory
    advisory_payload = {
        "name": "Test Farmer",
        "phone_number": "+919999988888",
        "crop": "rice",
        "crop_stage": "vegetative",
        "soil_type": "alluvial",
        "language": "English",
        "gps_location": {"latitude": 28.6139, "longitude": 77.2090},
    }
    headers = {"Authorization": f"Bearer {token}"}
    advisory_response = client.post("/advisory/", json=advisory_payload, headers=headers)
    assert advisory_response.status_code == 200
    advisory_data = advisory_response.json()
    assert advisory_data["status"] == "Advisory generation started"
    assert advisory_data["advisory"]["recommendation"] is not None
