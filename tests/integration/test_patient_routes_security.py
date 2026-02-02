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

        assert response.status_code == 401, f"VULNERABLE: /api/v1/patients/ is accessible without authentication! Status: {response.status_code}"

def test_create_patient_unauthenticated_access():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    payload = {
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

    with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
        mock_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_session

        response = client.post("/api/v1/patients/", json=payload)

        assert response.status_code == 401, f"VULNERABLE: /api/v1/patients/ (POST) accessible without auth! Status: {response.status_code}"

def test_list_patients_by_caregiver_unauthenticated_access():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    caregiver_id = "123e4567-e89b-12d3-a456-426614174000"

    with patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:
        mock_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_session

        # Mock repository response
        mock_session.query.return_value.filter.return_value.count.return_value = 0
        mock_session.query.return_value.filter.return_value.all.return_value = []

        response = client.get(f"/api/v1/patients/caregiver/{caregiver_id}")

        assert response.status_code == 401, f"VULNERABLE: /api/v1/patients/caregiver/{caregiver_id} accessible without auth! Status: {response.status_code}"
