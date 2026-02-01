import pytest
from src.main import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_list_users_requires_auth(client):
    """
    Test that list_users requires authentication.
    Expected to FAIL currently (returns 500/200 instead of 401).
    """
    response = client.get("/api/v1/users/")
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"

def test_get_user_requires_auth(client):
    """
    Test that get_user requires authentication.
    Expected to FAIL currently (returns 500/200/400 instead of 401).
    """
    # Use a dummy UUID
    response = client.get("/api/v1/users/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
