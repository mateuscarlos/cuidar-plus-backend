"""Script to create all database tables."""
from src.infrastructure.database.session import Base, engine

# Import all models to register them with Base.metadata
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.models.patient_model import PatientModel
from src.infrastructure.database.models.medication_model import MedicationModel
from src.infrastructure.database.models.appointment_model import AppointmentModel
from src.infrastructure.database.models.insurer_model import InsurerModel
from src.infrastructure.database.models.provider_model import ProviderModel
from src.infrastructure.database.models.inventory_item_model import InventoryItemModel
from src.infrastructure.database.models.report_model import ReportModel

if __name__ == "__main__":
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ All tables created successfully!")
    
    # Verify tables were created
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"\nTables in database: {tables}")
