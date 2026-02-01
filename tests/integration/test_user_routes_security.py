import pytest
from unittest.mock import MagicMock, patch
from src.main import create_app

def test_list_users_unauthenticated_access():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    with patch("src.presentation.api.v1.routes.user_routes.get_db_context") as mock_db:
        mock_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_session

        # Mock the repository call to return empty list
        mock_session.query.return_value.offset.return_value.limit.return_value.all.return_value = []
        mock_session.query.return_value.count.return_value = 0

        response = client.get("/api/v1/users/")

        if response.status_code == 200:
            pytest.fail("VULNERABLE: /api/v1/users/ is accessible without authentication!")

        assert response.status_code == 401, f"Expected 401, got {response.status_code}"

def test_get_user_unauthenticated_access():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    user_id = "123e4567-e89b-12d3-a456-426614174000"

    with patch("src.presentation.api.v1.routes.user_routes.get_db_context") as mock_db:
        mock_session = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_session

        # We need to mock enough to get 200 OK if vulnerable
        # But even if we don't, if we get anything other than 401, it's vulnerable (because auth check comes first)

        response = client.get(f"/api/v1/users/{user_id}")

        if response.status_code != 401:
             pytest.fail(f"VULNERABLE: /api/v1/users/{user_id} does not require authentication! Status: {response.status_code}")
