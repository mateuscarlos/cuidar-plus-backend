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

        # Mock the repository call to return empty list
        mock_session.query.return_value.offset.return_value.limit.return_value.all.return_value = []
        mock_session.query.return_value.count.return_value = 0

        response = client.get("/api/v1/patients/")

        if response.status_code == 200:
            pytest.fail("VULNERABLE: /api/v1/patients/ is accessible without authentication!")

        assert response.status_code == 401, f"Expected 401, got {response.status_code}"

def test_create_patient_unauthenticated_access():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    payload = {
        "caregiver_id": "123e4567-e89b-12d3-a456-426614174000",
        "full_name": "Test Patient",
        "cpf": "123.456.789-00",
        "date_of_birth": "1950-05-15",
        "gender": "M",
        "address": "Test Address",
        "phone": "(11) 98765-4321",
        "emergency_contact": "Emergency",
        "emergency_phone": "(11) 91234-5678"
    }

    with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
        mock_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_session

        # Mock dependencies for creating patient
        # We assume if it reaches DB, it's vulnerable.
        # Even if it fails validation, it should fail AUTH first.

        response = client.post("/api/v1/patients/", json=payload)

        if response.status_code == 201 or response.status_code == 200:
             pytest.fail("VULNERABLE: /api/v1/patients/ (POST) is accessible without authentication!")

        # If it returns 400 (validation error) instead of 401, it is ALSO vulnerable because it processed the input.
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"

def test_list_patients_by_caregiver_unauthenticated_access():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    caregiver_id = "123e4567-e89b-12d3-a456-426614174000"

    with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
        mock_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_session

        # Mock the use case execution
        # Since the route uses a repository and use case, mocking session might be enough if repo uses session
        # But here we just want to ensure 401 is returned before any logic.

        response = client.get(f"/api/v1/patients/caregiver/{caregiver_id}")

        if response.status_code == 200:
             pytest.fail(f"VULNERABLE: /api/v1/patients/caregiver/{caregiver_id} is accessible without authentication!")

        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
