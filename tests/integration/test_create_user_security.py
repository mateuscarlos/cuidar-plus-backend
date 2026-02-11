import pytest
from unittest.mock import MagicMock, patch
from src.config import Settings

def test_create_user_unauthenticated_access_is_blocked():
    """
    Test that unauthenticated requests to create a user are blocked.
    Regression test for Critical Vulnerability: Unauthenticated User Creation.
    """
    # Mock settings to return production environment to enforce auth
    mock_settings = Settings()
    mock_settings.FLASK_ENV = "production"

    # Patch settings in both src.main and the middleware module where it's used
    with patch("src.main.settings", mock_settings), \
         patch("src.presentation.api.middlewares.auth_middleware.settings", mock_settings):

        from src.main import create_app

        app = create_app()
        app.config["TESTING"] = True
        client = app.test_client()

        new_user_payload = {
            "email": "hacker@example.com",
            "password": "password123",
            "full_name": "Hacker Admin",
            "role": "admin"
        }

        # Mock the database context and repository just in case auth fails (defense in depth)
        # But we expect the request to be stopped BEFORE hitting the DB
        with patch("src.presentation.api.v1.routes.user_routes.get_db_context") as mock_db:

            # Attempt to create user without Auth header
            response = client.post("/api/v1/users/", json=new_user_payload)

            # Should be 401 Unauthorized
            assert response.status_code == 401, f"Expected 401, got {response.status_code}. Endpoint is vulnerable!"

            # Ensure error message is standard
            data = response.get_json()
            assert "error" in data
            assert "Authorization header is missing" in data["error"]

def test_create_user_non_admin_access_is_forbidden():
    """
    Test that authenticated users WITHOUT 'admin' role are forbidden from creating users.
    Regression test for Critical Vulnerability: Privilege Escalation / Authorization Bypass.
    """
    # Mock settings to return production environment to enforce auth
    mock_settings = Settings()
    mock_settings.FLASK_ENV = "production"
    mock_settings.JWT_SECRET_KEY = "test_secret"
    mock_settings.JWT_ALGORITHM = "HS256"

    # Patch settings
    with patch("src.main.settings", mock_settings), \
         patch("src.presentation.api.middlewares.auth_middleware.settings", mock_settings):

        from src.main import create_app

        app = create_app()
        app.config["TESTING"] = True
        client = app.test_client()

        new_user_payload = {
            "email": "hacker@example.com",
            "password": "password123",
            "full_name": "Hacker Admin",
            "role": "admin"
        }

        # Mock JWTHandler to validate token but return non-admin role
        with patch("src.presentation.api.middlewares.auth_middleware.JWTHandler") as MockJWTHandler:
            mock_jwt = MockJWTHandler.return_value
            # return a payload with 'caregiver' role
            mock_jwt.decode_token.return_value = {
                "sub": "user-uuid",
                "email": "caregiver@example.com",
                "role": "caregiver",
                "type": "access"
            }

            # Attempt to create user WITH Auth header but WRONG role
            response = client.post(
                "/api/v1/users/",
                json=new_user_payload,
                headers={"Authorization": "Bearer valid_token"}
            )

            # Should be 403 Forbidden
            assert response.status_code == 403, f"Expected 403, got {response.status_code}. Role check failed!"

            data = response.get_json()
            assert "error" in data
            assert "Insufficient permissions" in data["error"]
