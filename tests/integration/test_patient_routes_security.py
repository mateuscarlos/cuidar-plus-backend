import pytest
from unittest.mock import MagicMock, patch
from src.main import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_list_patients_unauthenticated_access(client):
    """Verify that listing patients requires authentication."""
    # Force FLASK_ENV to be 'production' to ensure auth check is active
    with patch("src.presentation.api.middlewares.auth_middleware.settings.FLASK_ENV", "production"):
        with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
            mock_session = MagicMock()
            mock_db.return_value.__enter__.return_value = mock_session

            # Mock the repository call to return empty list (if it gets that far)
            mock_session.query.return_value.offset.return_value.limit.return_value.all.return_value = []
            mock_session.query.return_value.count.return_value = 0

            response = client.get("/api/v1/patients/")

            # This assertion will fail initially because the route is unprotected (returns 200)
            assert response.status_code == 401, f"Expected 401, got {response.status_code}"

def test_create_patient_unauthenticated_access(client):
    """Verify that creating a patient requires authentication."""
    with patch("src.presentation.api.middlewares.auth_middleware.settings.FLASK_ENV", "production"):
        response = client.post("/api/v1/patients/", json={
            "caregiver_id": "123e4567-e89b-12d3-a456-426614174000",
            "full_name": "Test Patient",
            "cpf": "123.456.789-00",
            "date_of_birth": "1980-01-01",
            "gender": "M",
            "address": "Test Address",
            "phone": "(11) 99999-9999",
            "emergency_contact": "Test Contact",
            "emergency_phone": "(11) 88888-8888"
        })

        assert response.status_code == 401, f"Expected 401, got {response.status_code}"

def test_list_patients_by_caregiver_unauthenticated_access(client):
    """Verify that listing patients by caregiver requires authentication."""
    caregiver_id = "123e4567-e89b-12d3-a456-426614174000"
    with patch("src.presentation.api.middlewares.auth_middleware.settings.FLASK_ENV", "production"):
        with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
             mock_session = MagicMock()
             mock_db.return_value.__enter__.return_value = mock_session

             response = client.get(f"/api/v1/patients/caregiver/{caregiver_id}")

             assert response.status_code == 401, f"Expected 401, got {response.status_code}"

def test_list_patients_authorized_access(client):
    """Verify that listing patients works with valid authentication."""
    with patch("src.presentation.api.middlewares.auth_middleware.settings.FLASK_ENV", "production"):
        with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
            mock_session = MagicMock()
            mock_db.return_value.__enter__.return_value = mock_session

            # Mock the repository call to return empty list
            mock_session.query.return_value.offset.return_value.limit.return_value.all.return_value = []
            mock_session.query.return_value.count.return_value = 0

            # Create a valid token (or mock the decode function)
            with patch("src.presentation.api.middlewares.auth_middleware.JWTHandler") as MockJWTHandler:
                mock_jwt = MockJWTHandler.return_value
                mock_jwt.decode_token.return_value = {
                    "sub": "user-id",
                    "email": "test@example.com",
                    "role": "caregiver",
                    "type": "access"
                }

                headers = {"Authorization": "Bearer valid-token"}
                response = client.get("/api/v1/patients/", headers=headers)

                assert response.status_code == 200, f"Expected 200, got {response.status_code}"
