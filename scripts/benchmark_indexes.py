import sys
import os
import time
import random
from uuid import uuid4
from datetime import datetime, timedelta

# Add root directory to path to allow imports
sys.path.append(os.getcwd())

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.infrastructure.database.models.patient_model import PatientModel
from src.infrastructure.database.models.appointment_model import AppointmentModel
from src.infrastructure.database.session import Base
from src.infrastructure.database.models.user_model import UserModel

# Setup local benchmark DB
DB_URL = "sqlite:///benchmark.db"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_db():
    print("Setting up benchmark database...")
    if os.path.exists("benchmark.db"):
        os.remove("benchmark.db")

    # Create tables
    # Note: This will use the current definition of the models.
    # If the models have index=True, the index will be created.
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        # Create a dummy caregiver
        caregiver = UserModel(
            id=uuid4(),
            email=f"caregiver_{uuid4()}@example.com",
            password_hash="hash",
            full_name="Care Giver",
            role="caregiver",
            is_active=True
        )
        session.add(caregiver)
        session.commit()

        # Create 1000 patients
        print("Creating 1,000 patients...")
        patients = []
        caregiver_id = caregiver.id
        for i in range(1000):
            patient = PatientModel(
                id=uuid4(),
                caregiver_id=caregiver_id,
                full_name=f"Patient {i}",
                cpf=f"{i:011d}",
                date_of_birth=datetime.now().date(),
                gender="M",
                address="Address",
                phone="123",
                emergency_contact="Contact",
                emergency_phone="123"
            )
            patients.append(patient)
        session.add_all(patients)
        session.commit()

        # Create 10,000 appointments
        print("Creating 10,000 appointments...")
        appointments = []
        patient_ids = [p.id for p in patients]
        for i in range(10000):
            appt = AppointmentModel(
                id=uuid4(),
                patient_id=random.choice(patient_ids),
                title=f"Appointment {i}",
                appointment_date=datetime.now(),
                duration_minutes=30,
                location="Office",
                status="scheduled"
            )
            appointments.append(appt)

        # Batch insert appointments
        session.bulk_save_objects(appointments)
        session.commit()
        print("Database setup complete.")
    except Exception as e:
        print(f"Error setting up database: {e}")
        session.rollback()
        raise
    finally:
        session.close()

def run_benchmark():
    session = SessionLocal()

    try:
        # Get a random patient ID to query
        patient = session.query(PatientModel).first()
        if not patient:
            print("No patients found. Run with --setup first.")
            return

        patient_id = patient.id
        # Convert UUID to string for SQLite raw query if needed, but parameter binding is safer
        # SQLite stores UUIDs as char(32) or blob usually.
        # SQLAlchemy with UUID(as_uuid=True) handles conversion.

        print(f"\nBenchmarking query: Find appointments for patient_id={patient_id}")

        # Explain Query Plan
        print("\n--- EXPLAIN QUERY PLAN ---")
        conn = engine.raw_connection()
        cursor = conn.cursor()

        # The stored format depends on the driver, but typically it's the 32-char hex string for SQLite
        # However, let's look at how SQLAlchemy sends it.
        # We'll just pass the parameter.
        cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM appointments WHERE patient_id = ?", (str(patient_id),))
        rows = cursor.fetchall()
        for row in rows:
            print(row)
            # Tuple format: (id, parent, notused, detail)
        cursor.close()
        conn.close()

        # Measure execution time
        start_time = time.time()
        iterations = 100
        for _ in range(iterations):
            # Using ORM
            results = session.query(AppointmentModel).filter(AppointmentModel.patient_id == patient_id).all()
            _ = len(results)

        end_time = time.time()
        avg_time = (end_time - start_time) / iterations * 1000 # in ms

        print(f"\nAverage query time over {iterations} iterations: {avg_time:.4f} ms")
    finally:
        session.close()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        setup_db()

    run_benchmark()
