"""Database initialization script."""
from sqlalchemy import text

from src.infrastructure.database.session import engine, Base, SessionLocal
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.models.patient_model import PatientModel
from src.infrastructure.database.models.medication_model import MedicationModel
from src.infrastructure.database.models.appointment_model import AppointmentModel
from src.infrastructure.security.password_hasher import PasswordHasher
from src.shared.utils.logger import app_logger


def init_database():
    """
    Initialize database tables and create test data.
    
    This script should be run once to set up the database.
    """
    app_logger.info("Initializing database...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    app_logger.info("Database tables created successfully")
    
    # Create initial admin user (optional)
    create_admin_user()
    
    app_logger.info("Database initialization complete")


def create_admin_user():
    """Create an initial admin user if not exists."""
    session = SessionLocal()
    
    try:
        # Check if admin user already exists
        admin_email = "admin@cuidarplus.com"
        existing_admin = session.query(UserModel).filter(
            UserModel.email == admin_email
        ).first()
        
        if existing_admin:
            app_logger.info("Admin user already exists")
            return
        
        # Create admin user
        password_hasher = PasswordHasher()
        # Truncate password to 72 bytes (bcrypt limit)
        password = "admin123"[:72]
        admin_user = UserModel(
            email=admin_email,
            password_hash=password_hasher.hash(password),  # Change in production!
            full_name="System Administrator",
            role="admin",
            is_active=True,
        )
        
        session.add(admin_user)
        session.commit()
        
        app_logger.info(f"Admin user created: {admin_email}")
        app_logger.warning("Default password is 'admin123' - CHANGE IT IN PRODUCTION!")
    
    except Exception as e:
        session.rollback()
        app_logger.error(f"Error creating admin user: {e}")
        raise
    finally:
        session.close()


def drop_all_tables():
    """Drop all database tables (use with caution!)."""
    app_logger.warning("Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    app_logger.info("All tables dropped")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--drop":
        drop_all_tables()
    
    init_database()
