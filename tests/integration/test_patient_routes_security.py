import pytest
from unittest.mock import MagicMock, patch
from src.main import create_app

def test_list_patients_unauthenticated_access():
    # Patch the settings in the middleware module to ensure we are in production mode
    # effectively disabling the development bypass
    with patch("src.presentation.api.middlewares.auth_middleware.settings") as mock_settings:
        mock_settings.FLASK_ENV = "production"

        app = create_app()
        app.config["TESTING"] = True
        client = app.test_client()

        # Mock the database to handle the case where the endpoint is vulnerable
        # If vulnerable, it will try to query the database.
        with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
            mock_session = MagicMock()
            mock_db.return_value.__enter__.return_value = mock_session

            # Mock the repository call to return empty list
            mock_session.query.return_value.offset.return_value.limit.return_value.all.return_value = []
            mock_session.query.return_value.count.return_value = 0

            response = client.get("/api/v1/patients/")

            if response.status_code == 200:
                pytest.fail("VULNERABLE: /api/v1/patients/ is accessible without authentication!")

            assert response.status_code == 401, f"Expected 401, got {response.status_code}"

def test_create_patient_unauthenticated_access():
    with patch("src.presentation.api.middlewares.auth_middleware.settings") as mock_settings:
        mock_settings.FLASK_ENV = "production"

        app = create_app()
        app.config["TESTING"] = True
        client = app.test_client()

        data = {
            "caregiver_id": "123e4567-e89b-12d3-a456-426614174000",
            "full_name": "Maria Silva",
            "cpf": "123.456.789-00",
            "date_of_birth": "1950-05-15",
            "gender": "F",
            "address": "Rua Example, 123",
            "phone": "(11) 98765-4321",
            "emergency_contact": "João Silva",
            "emergency_phone": "(11) 91234-5678"
        }

        # Mock DB for vulnerable case
        with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
             # We don't need detailed mocks if we expect 401, but preventing crash if 200 is good.
            mock_session = MagicMock()
            mock_db.return_value.__enter__.return_value = mock_session

            response = client.post("/api/v1/patients/", json=data)

            if response.status_code == 201 or response.status_code == 400: # 400 if validation fails but auth passed
                 pytest.fail(f"VULNERABLE: /api/v1/patients/ (POST) is accessible without authentication! Status: {response.status_code}")

            assert response.status_code == 401, f"Expected 401, got {response.status_code}"

def test_list_patients_by_caregiver_unauthenticated_access():
    with patch("src.presentation.api.middlewares.auth_middleware.settings") as mock_settings:
        mock_settings.FLASK_ENV = "production"

        app = create_app()
        app.config["TESTING"] = True
        client = app.test_client()

        caregiver_id = "123e4567-e89b-12d3-a456-426614174000"

        with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
            mock_session = MagicMock()
            mock_db.return_value.__enter__.return_value = mock_session

            # Mock return for vulnerable case
            mock_session.query.return_value.filter.return_value.all.return_value = []

            response = client.get(f"/api/v1/patients/caregiver/{caregiver_id}")

            if response.status_code == 200:
                pytest.fail(f"VULNERABLE: /api/v1/patients/caregiver/{caregiver_id} is accessible without authentication!")

            assert response.status_code == 401, f"Expected 401, got {response.status_code}"
