import pytest
from unittest.mock import MagicMock, patch
from src.main import create_app
from uuid import uuid4

def test_list_patients_unauthenticated_access():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
        mock_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_session

        response = client.get("/api/v1/patients/")

        if response.status_code != 401:
            pytest.fail(f"VULNERABLE: /api/v1/patients/ is accessible without authentication! Status: {response.status_code}")

def test_create_patient_unauthenticated_access():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
        mock_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_session

        data = {
            "caregiver_id": str(uuid4()),
            "full_name": "Test Patient",
            "cpf": "123.456.789-00",
            "date_of_birth": "1990-01-01",
            "gender": "M",
            "address": "Test St",
            "phone": "123456789",
            "emergency_contact": "Emergency",
            "emergency_phone": "987654321"
        }

        response = client.post("/api/v1/patients/", json=data)

        if response.status_code != 401:
            pytest.fail(f"VULNERABLE: POST /api/v1/patients/ is accessible without authentication! Status: {response.status_code}")

def test_list_patients_by_caregiver_unauthenticated_access():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    caregiver_id = str(uuid4())

    with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
        mock_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_session

        response = client.get(f"/api/v1/patients/caregiver/{caregiver_id}")

        if response.status_code != 401:
            pytest.fail(f"VULNERABLE: /api/v1/patients/caregiver/{caregiver_id} is accessible without authentication! Status: {response.status_code}")
