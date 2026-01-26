"""Reports Routes."""
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta

from src.infrastructure.database.session import get_db_context

reports_bp = Blueprint("reports", __name__, url_prefix="/api/v1/reports")


@reports_bp.route("/", methods=["GET"])
def list_reports():
    """
    List all available reports.
    """
    reports = [
        {
            "id": "patients-summary",
            "name": "Resumo de Pacientes",
            "description": "Estatísticas gerais sobre pacientes",
            "endpoint": "/api/v1/reports/summary"
        },
        {
            "id": "medications-schedule",
            "name": "Agenda de Medicamentos",
            "description": "Horários de medicação por paciente",
            "endpoint": "/api/v1/reports/medications"
        },
        {
            "id": "appointments-calendar",
            "name": "Calendário de Consultas",
            "description": "Consultas agendadas",
            "endpoint": "/api/v1/reports/appointments"
        }
    ]
    
    return jsonify({
        "data": reports,
        "pagination": {
            "total": len(reports),
            "page": 1,
            "pageSize": len(reports),
            "totalPages": 1
        }
    }), 200


@reports_bp.route("/summary", methods=["GET"])
def get_summary():
    """
    Get summary statistics about patients, medications, and appointments.
    """
    try:
        with get_db_context() as session:
            from src.infrastructure.database.models.patient_model import PatientModel
            from src.infrastructure.database.models.medication_model import MedicationModel
            from src.infrastructure.database.models.appointment_model import AppointmentModel
            
            # Count totals
            total_patients = session.query(PatientModel).count()
            active_patients = session.query(PatientModel).filter(PatientModel.is_active == True).count()
            total_medications = session.query(MedicationModel).count()
            active_medications = session.query(MedicationModel).filter(MedicationModel.is_active == True).count()
            
            # Count appointments
            total_appointments = session.query(AppointmentModel).count()
            upcoming_appointments = session.query(AppointmentModel).filter(
                AppointmentModel.appointment_date >= datetime.now()
            ).count()
            
            return jsonify({
                "patients": {
                    "total": total_patients,
                    "active": active_patients,
                    "inactive": total_patients - active_patients
                },
                "medications": {
                    "total": total_medications,
                    "active": active_medications,
                    "inactive": total_medications - active_medications
                },
                "appointments": {
                    "total": total_appointments,
                    "upcoming": upcoming_appointments,
                    "completed": total_appointments - upcoming_appointments
                },
                "generated_at": datetime.now().isoformat()
            }), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@reports_bp.route("/summary/start-date/<start_date>/end-date/<end_date>", methods=["GET"])
def get_summary_by_period(start_date: str, end_date: str):
    """
    Get summary statistics for a specific period.
    """
    try:
        start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        with get_db_context() as session:
            from src.infrastructure.database.models.patient_model import PatientModel
            from src.infrastructure.database.models.appointment_model import AppointmentModel
            
            # Patients created in period
            patients_created = session.query(PatientModel).filter(
                PatientModel.created_at >= start,
                PatientModel.created_at <= end
            ).count()
            
            # Appointments in period
            appointments_period = session.query(AppointmentModel).filter(
                AppointmentModel.appointment_date >= start,
                AppointmentModel.appointment_date <= end
            ).count()
            
            return jsonify({
                "period": {
                    "start": start_date,
                    "end": end_date
                },
                "patients_created": patients_created,
                "appointments": appointments_period,
                "generated_at": datetime.now().isoformat()
            }), 200
    
    except ValueError as e:
        return jsonify({"error": "Invalid date format", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
