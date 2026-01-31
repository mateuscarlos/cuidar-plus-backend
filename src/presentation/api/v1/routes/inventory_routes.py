"""Medication/Inventory Routes."""
from flask import Blueprint, request, jsonify
from uuid import UUID
from datetime import datetime

from src.infrastructure.database.session import get_db_context
from src.presentation.api.middlewares.auth_middleware import require_auth

inventory_bp = Blueprint("inventory", __name__, url_prefix="/api/v1/inventory")


@inventory_bp.route("/", methods=["GET"])
@require_auth
def list_inventory():
    """
    List all medications (inventory) with pagination.
    """
    try:
        page = request.args.get("page", 1, type=int)
        page_size = request.args.get("pageSize", 20, type=int)
        
        with get_db_context() as session:
            from src.infrastructure.database.models.medication_model import MedicationModel
            medications = session.query(MedicationModel).offset((page - 1) * page_size).limit(page_size).all()
            total = session.query(MedicationModel).count()
            
            return jsonify({
                "data": [
                    {
                        "id": str(med.id),
                        "patient_id": str(med.patient_id),
                        "name": med.name,
                        "dosage": med.dosage,
                        "frequency": med.frequency,
                        "start_date": med.start_date.isoformat(),
                        "end_date": med.end_date.isoformat() if med.end_date else None,
                        "is_active": med.is_active,
                    }
                    for med in medications
                ],
                "pagination": {
                    "total": total,
                    "page": page,
                    "pageSize": page_size,
                    "totalPages": (total + page_size - 1) // page_size
                }
            }), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@inventory_bp.route("/patient/<patient_id>", methods=["GET"])
@require_auth
def list_inventory_by_patient(patient_id: str):
    """
    List medications for a specific patient.
    """
    try:
        patient_uuid = UUID(patient_id)
        
        with get_db_context() as session:
            from src.infrastructure.database.models.medication_model import MedicationModel
            medications = session.query(MedicationModel).filter(
                MedicationModel.patient_id == patient_uuid
            ).all()
            
            return jsonify({
                "medications": [
                    {
                        "id": str(med.id),
                        "patient_id": str(med.patient_id),
                        "name": med.name,
                        "dosage": med.dosage,
                        "frequency": med.frequency,
                        "schedule_times": med.schedule_times,
                        "start_date": med.start_date.isoformat(),
                        "end_date": med.end_date.isoformat() if med.end_date else None,
                        "instructions": med.instructions,
                        "is_active": med.is_active,
                    }
                    for med in medications
                ],
                "total": len(medications),
            }), 200
    
    except ValueError:
        return jsonify({"error": "Invalid patient ID format"}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
