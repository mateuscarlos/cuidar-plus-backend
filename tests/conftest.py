"""Test configuration and fixtures."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.infrastructure.database.session import Base


@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine."""
    # Use in-memory SQLite for tests
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def test_session(test_engine):
    """Create a test database session."""
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestSessionLocal()
    
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@pytest.fixture
def sample_user_data():
    """Sample user data for tests."""
    return {
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User",
        "role": "caregiver",
    }


@pytest.fixture
def sample_patient_data():
    """Sample patient data for tests."""
    from datetime import date
    from uuid import uuid4
    
    return {
        "caregiver_id": uuid4(),
        "full_name": "Maria Silva",
        "cpf": "12345678901",
        "date_of_birth": date(1950, 5, 15),
        "gender": "F",
        "address": "Rua Example, 123",
        "phone": "11987654321",
        "emergency_contact": "João Silva",
        "emergency_phone": "11912345678",
    }
