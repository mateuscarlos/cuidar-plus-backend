"""Patient Routes."""
import logging
from flask import Blueprint, request, jsonify
from uuid import UUID
from datetime import datetime

from src.application.use_cases.patients.create_patient import (
    CreatePatientInput,
    CreatePatientUseCase,
)
from src.application.use_cases.patients.list_patients import ListPatientsByCaregiverUseCase
from src.infrastructure.database.session import get_db_context
from src.infrastructure.repositories.sqlalchemy_patient_repository import SQLAlchemyPatientRepository
from src.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.shared.exceptions.application_exception import ApplicationException
from src.presentation.api.middlewares.auth_middleware import require_auth

patient_bp = Blueprint("patients", __name__, url_prefix="/api/v1/patients")
logger = logging.getLogger(__name__)

@patient_bp.route("/", methods=["GET"])
@require_auth
def list_all_patients():
    """
    List all patients with pagination.
    """
    try:
        page = request.args.get("page", 1, type=int)
        page_size = request.args.get("pageSize", 20, type=int)

        with get_db_context() as session:
            from src.infrastructure.database.models.patient_model import PatientModel
            patients = session.query(PatientModel).offset((page - 1) * page_size).limit(page_size).all()
            total = session.query(PatientModel).count()

            return jsonify({
                "data": [
                    {
                        "id": str(patient.id),
                        "caregiver_id": str(patient.caregiver_id),
                        "full_name": patient.full_name,
                        "cpf": patient.cpf,
                        "date_of_birth": patient.date_of_birth.isoformat(),
                        "gender": patient.gender,
                        "phone": patient.phone,
                        "is_active": patient.is_active,
                        "created_at": patient.created_at.isoformat(),
                    }
                    for patient in patients
                ],
                "pagination": {
                    "total": total,
                    "page": page,
                    "pageSize": page_size,
                    "totalPages": (total + page_size - 1) // page_size
                }
            }), 200

    except Exception as e:
        logger.error(f"Error listing patients: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@patient_bp.route("/", methods=["POST"])
@require_auth
def create_patient():
    """
    Create a new patient.

    Request body:
    {
        "caregiver_id": "...",
        "full_name": "Maria Silva",
        "cpf": "123.456.789-00",
        "date_of_birth": "1950-05-15",
        "gender": "F",
        "address": "Rua Example, 123",
        "phone": "(11) 98765-4321",
        "emergency_contact": "João Silva",
        "emergency_phone": "(11) 91234-5678",
        "medical_conditions": "Hipertensão, Diabetes",
        "allergies": "Penicilina",
        "observations": "Paciente lúcida e orientada"
    }
    """
    try:
        data = request.get_json()

        required_fields = [
            "caregiver_id", "full_name", "cpf", "date_of_birth", "gender",
            "address", "phone", "emergency_contact", "emergency_phone"
        ]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Parse date
        date_of_birth = datetime.strptime(data["date_of_birth"], "%Y-%m-%d").date()

        input_dto = CreatePatientInput(
            caregiver_id=UUID(data["caregiver_id"]),
            full_name=data["full_name"],
            cpf=data["cpf"],
            date_of_birth=date_of_birth,
            gender=data["gender"],
            address=data["address"],
            phone=data["phone"],
            emergency_contact=data["emergency_contact"],
            emergency_phone=data["emergency_phone"],
            medical_conditions=data.get("medical_conditions"),
            allergies=data.get("allergies"),
            observations=data.get("observations"),
        )

        with get_db_context() as session:
            patient_repository = SQLAlchemyPatientRepository(session)
            user_repository = SQLAlchemyUserRepository(session)

            use_case = CreatePatientUseCase(patient_repository, user_repository)
            output = use_case.execute(input_dto)

            return jsonify({
                "id": str(output.id),
                "caregiver_id": str(output.caregiver_id),
                "full_name": output.full_name,
                "cpf": output.cpf,
                "age": output.age,
                "gender": output.gender,
            }), 201

    except ApplicationException as e:
        logger.warning(f"Application error creating patient: {e.message}")
        return jsonify({"error": e.message, "code": e.code}), 400
    except ValueError as e:
        logger.warning(f"Validation error creating patient: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating patient: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@patient_bp.route("/caregiver/<caregiver_id>", methods=["GET"])
@require_auth
def list_patients_by_caregiver(caregiver_id: str):
    """
    List all patients for a specific caregiver.

    Response:
    {
        "patients": [
            {
                "id": "...",
                "full_name": "Maria Silva",
                "age": 74,
                "gender": "F",
                "is_active": true
            }
        ],
        "total": 1
    }
    """
    try:
        caregiver_uuid = UUID(caregiver_id)

        with get_db_context() as session:
            patient_repository = SQLAlchemyPatientRepository(session)
            use_case = ListPatientsByCaregiverUseCase(patient_repository)
            output = use_case.execute(caregiver_uuid)

            return jsonify({
                "patients": [
                    {
                        "id": str(p.id),
                        "full_name": p.full_name,
                        "age": p.age,
                        "gender": p.gender,
                        "is_active": p.is_active,
                    }
                    for p in output.patients
                ],
                "total": output.total,
            }), 200

    except ValueError:
        return jsonify({"error": "Invalid caregiver ID format"}), 400
    except Exception as e:
        logger.error(f"Error listing patients by caregiver: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
