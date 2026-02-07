import sys
import os
import time
import uuid
import random
from datetime import date, datetime

# Ensure we can import from src
sys.path.append(os.getcwd())

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from faker import Faker

from src.infrastructure.database.session import Base
from src.infrastructure.database.models.patient_model import PatientModel
from src.infrastructure.database.models.user_model import UserModel

# Setup
fake = Faker()
engine = create_engine("sqlite:///benchmark.db") # Use file DB so we can inspect if needed, or re-use
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_db():
    if os.path.exists("benchmark.db"):
        os.remove("benchmark.db")
    Base.metadata.create_all(bind=engine)

def seed_data(num_caregivers=50, patients_per_caregiver=200):
    session = SessionLocal()

    caregivers = []
    print(f"Creating {num_caregivers} caregivers...")
    for _ in range(num_caregivers):
        caregiver = UserModel(
            email=fake.email(),
            password_hash="hash",
            full_name=fake.name(),
            role="caregiver",
            is_active=True
        )
        session.add(caregiver)
        caregivers.append(caregiver)
    session.commit() # Commit to get IDs

    print(f"Creating {num_caregivers * patients_per_caregiver} patients...")
    patients = []
    for caregiver in caregivers:
        for _ in range(patients_per_caregiver):
            patient = PatientModel(
                caregiver_id=caregiver.id,
                full_name=fake.name(),
                cpf=fake.ssn(), # Faker might not have valid CPF, but string is fine
                date_of_birth=date(1990, 1, 1),
                gender="M",
                address=fake.address(),
                phone=fake.phone_number(),
                emergency_contact=fake.name(),
                emergency_phone=fake.phone_number(),
                is_active=True
            )
            patients.append(patient)

        if len(patients) >= 1000:
            session.add_all(patients)
            session.commit()
            patients = []

    if patients:
        session.add_all(patients)
        session.commit()

    print("Data seeded.")
    return [c.id for c in caregivers]

def benchmark_query(caregiver_ids):
    session = SessionLocal()
    start_time = time.time()

    # Query for each caregiver multiple times to average out
    iterations = 0

    # Select a random subset of caregivers to query
    target_caregivers = random.sample(caregiver_ids, min(10, len(caregiver_ids)))

    for caregiver_id in target_caregivers:
        # Run the query we want to optimize
        stmt = select(PatientModel).where(PatientModel.caregiver_id == caregiver_id)
        results = session.execute(stmt).scalars().all()
        iterations += 1

    end_time = time.time()
    session.close()

    total_time = end_time - start_time
    avg_time = total_time / iterations
    print(f"Average query time: {avg_time:.6f} seconds ({iterations} iterations)")
    return avg_time

if __name__ == "__main__":
    setup_db()
    caregiver_ids = seed_data()

    print("\nBenchmarking...")
    # Warmup
    benchmark_query(caregiver_ids)

    # Actual run
    times = []
    for _ in range(5):
        times.append(benchmark_query(caregiver_ids))

    print(f"\nAverage over 5 runs: {sum(times)/len(times):.6f} seconds")
