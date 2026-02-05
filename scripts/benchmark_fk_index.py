import sys
import os
import time
from uuid import uuid4
from datetime import datetime

# Add root to path
sys.path.append(os.getcwd())

from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.database.session import Base
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.models.patient_model import PatientModel
from src.infrastructure.database.models.appointment_model import AppointmentModel
from src.infrastructure.database.models.medication_model import MedicationModel

def run_benchmark():
    # Use a file-based SQLite db to persist (though we delete it each run)
    db_path = "benchmark.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        print("Seeding data...")
        # Create caregiver
        caregiver = UserModel(
            id=uuid4(),
            email=f"caregiver_{uuid4()}@test.com",
            password_hash="hash",
            full_name="Care Giver",
            role="caregiver"
        )
        session.add(caregiver)
        session.flush()

        # Create patients
        patients = []
        for i in range(10):
            p = PatientModel(
                id=uuid4(),
                caregiver_id=caregiver.id,
                full_name=f"Patient {i}",
                cpf=str(uuid4())[:11],
                date_of_birth=datetime.now(),
                gender="M",
                address="Addr",
                phone="123",
                emergency_contact="EC",
                emergency_phone="123"
            )
            patients.append(p)
        session.add_all(patients)
        session.flush()

        # Create appointments and medications
        appointments = []
        medications = []
        target_patient = patients[0]

        # Add data for other patients
        for p in patients[1:]:
            # Appointments
            for i in range(100):
                app = AppointmentModel(
                    id=uuid4(),
                    patient_id=p.id,
                    title="Checkup",
                    appointment_date=datetime.now(),
                    duration_minutes=30,
                    location="Clinic"
                )
                appointments.append(app)

            # Medications
            for i in range(50):
                med = MedicationModel(
                    id=uuid4(),
                    patient_id=p.id,
                    name="Aspirin",
                    dosage="100mg",
                    frequency="Daily",
                    schedule_times=[],
                    start_date=datetime.now()
                )
                medications.append(med)

        # Add data for target patient
        for i in range(10):
            app = AppointmentModel(
                id=uuid4(),
                patient_id=target_patient.id,
                title="Target Checkup",
                appointment_date=datetime.now(),
                duration_minutes=30,
                location="Clinic"
            )
            appointments.append(app)

            med = MedicationModel(
                id=uuid4(),
                patient_id=target_patient.id,
                name="Aspirin",
                dosage="100mg",
                frequency="Daily",
                schedule_times=[],
                start_date=datetime.now()
            )
            medications.append(med)

        session.add_all(appointments)
        session.add_all(medications)
        session.commit()
        print(f"Seeded {len(appointments)} appointments and {len(medications)} medications.")

        target_patient_id = target_patient.id
        target_caregiver_id = caregiver.id

        print("\n--- Benchmarking AppointmentModel.patient_id ---")
        result = session.execute(text(f"EXPLAIN QUERY PLAN SELECT * FROM appointments WHERE patient_id = '{target_patient_id}'"))
        for row in result:
            print(f"Appointment Query Plan: {row}")

        print("\n--- Benchmarking MedicationModel.patient_id ---")
        result = session.execute(text(f"EXPLAIN QUERY PLAN SELECT * FROM medications WHERE patient_id = '{target_patient_id}'"))
        for row in result:
            print(f"Medication Query Plan: {row}")

        print("\n--- Benchmarking PatientModel.caregiver_id ---")
        result = session.execute(text(f"EXPLAIN QUERY PLAN SELECT * FROM patients WHERE caregiver_id = '{target_caregiver_id}'"))
        for row in result:
            print(f"Patient Query Plan: {row}")

    finally:
        session.close()
        if os.path.exists(db_path):
            os.remove(db_path)

if __name__ == "__main__":
    run_benchmark()
