import pytest
from unittest.mock import MagicMock, patch
from src.main import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_list_patients_unauthenticated(client):
    """Verify that listing patients requires authentication."""
    # Mock settings in the middleware to force production mode
    with patch("src.presentation.api.middlewares.auth_middleware.settings") as mock_settings:
        mock_settings.FLASK_ENV = "production"

        response = client.get("/api/v1/patients/")

        # This assertion expects 401. If the route is unprotected, it will be 200.
        assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_create_patient_unauthenticated(client):
    """Verify that creating a patient requires authentication."""
    with patch("src.presentation.api.middlewares.auth_middleware.settings") as mock_settings:
        mock_settings.FLASK_ENV = "production"

        response = client.post("/api/v1/patients/", json={})
        assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_list_patients_by_caregiver_unauthenticated(client):
    """Verify that listing patients by caregiver requires authentication."""
    with patch("src.presentation.api.middlewares.auth_middleware.settings") as mock_settings:
        mock_settings.FLASK_ENV = "production"

        response = client.get("/api/v1/patients/caregiver/123e4567-e89b-12d3-a456-426614174000")
        assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_list_patients_authenticated(client):
    """Verify that authenticated requests can access the patient list."""
    with patch("src.presentation.api.middlewares.auth_middleware.settings") as mock_settings, \
         patch("src.presentation.api.middlewares.auth_middleware.JWTHandler") as MockJWTHandler, \
         patch("src.presentation.api.v1.routes.patient_routes.get_db_context") as mock_db:

        # 1. Force production mode
        mock_settings.FLASK_ENV = "production"

        # 2. Mock JWT validation
        mock_jwt_instance = MockJWTHandler.return_value
        mock_jwt_instance.decode_token.return_value = {
            "sub": "user-uuid",
            "email": "test@example.com",
            "role": "admin",
            "type": "access"
        }

        # 3. Mock Database
        mock_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_session

        # Mock query chain: session.query().offset().limit().all() -> []
        mock_query = mock_session.query.return_value
        mock_offset = mock_query.offset.return_value
        mock_limit = mock_offset.limit.return_value
        mock_limit.all.return_value = []

        # Mock count: session.query().count() -> 0
        mock_query.count.return_value = 0

        # Make the request with a fake token
        headers = {"Authorization": "Bearer fake-valid-token"}
        response = client.get("/api/v1/patients/", headers=headers)

        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Error: {response.get_json()}"
