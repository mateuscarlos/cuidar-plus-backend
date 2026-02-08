import pytest
from unittest.mock import MagicMock, patch
from src.main import create_app

def test_list_patients_unauthenticated_access():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
        mock_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_session

        # Mock query chain for list_all_patients
        # patients = session.query(PatientModel).offset(...).limit(...).all()
        # total = session.query(PatientModel).count()
        mock_session.query.return_value.offset.return_value.limit.return_value.all.return_value = []
        mock_session.query.return_value.count.return_value = 0

        response = client.get("/api/v1/patients/")

        # If we get 200, it means we accessed the resource without auth -> VULNERABLE
        # If we get 500, we also accessed the resource (but it crashed) -> VULNERABLE
        # We only want 401.

        assert response.status_code == 401, f"Expected 401 (Unauthorized), but got {response.status_code}. The endpoint is likely unprotected."

def test_create_patient_unauthenticated_access():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    payload = {
        "caregiver_id": "123e4567-e89b-12d3-a456-426614174000",
        "full_name": "Test Patient",
        "cpf": "123.456.789-00",
        "date_of_birth": "1950-01-01",
        "gender": "M",
        "address": "Test St",
        "phone": "1234567890",
        "emergency_contact": "Emergency",
        "emergency_phone": "0987654321"
    }

    with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
        mock_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_session

        # We don't need to mock the full creation logic perfectly, just enough to not crash immediately
        # if the auth check is missing.
        # But even if it crashes (500), it's not 401.

        response = client.post("/api/v1/patients/", json=payload)

        assert response.status_code == 401, f"Expected 401 (Unauthorized), but got {response.status_code}. The endpoint is likely unprotected."

def test_list_patients_by_caregiver_unauthenticated_access():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    caregiver_id = "123e4567-e89b-12d3-a456-426614174000"

    with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
        mock_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_session

        # Mocking for use case execution if needed, but again, checking for not 401

        response = client.get(f"/api/v1/patients/caregiver/{caregiver_id}")

        assert response.status_code == 401, f"Expected 401 (Unauthorized), but got {response.status_code}. The endpoint is likely unprotected."
