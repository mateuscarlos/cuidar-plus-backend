"""Provider Routes."""
from flask import Blueprint, jsonify, request
from uuid import UUID

from src.infrastructure.database.session import get_db_context
from src.infrastructure.database.models.provider_model import ProviderModel

provider_bp = Blueprint("providers", __name__, url_prefix="/api/v1/providers")


@provider_bp.route("/", methods=["GET"])
def list_providers():
    """List providers with filters."""
    try:
        page = request.args.get("page", 1, type=int)
        page_size = request.args.get("pageSize", 50, type=int)
        search = request.args.get("search")
        
        with get_db_context() as session:
            query = session.query(ProviderModel)
            
            if search:
                search_filter = f"%{search}%"
                query = query.filter(
                    ProviderModel.name.ilike(search_filter) |
                    ProviderModel.trade_name.ilike(search_filter)
                )
            
            total = query.count()
            providers = query.offset((page - 1) * page_size).limit(page_size).all()
            
            return jsonify({
                "data": [
                    {
                        "id": str(provider.id),
                        "name": provider.name,
                        "tradeName": provider.trade_name,
                        "type": provider.type,
                        "status": provider.status,
                        "phone": provider.phone,
                        "email": provider.email,
                        "hasEmergency": provider.has_emergency,
                        "rating": provider.rating,
                    }
                    for provider in providers
                ],
                "pagination": {
                    "total": total,
                    "page": page,
                    "pageSize": page_size,
                    "totalPages": (total + page_size - 1) // page_size,
                }
            }), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@provider_bp.route("/<provider_id>", methods=["GET"])
def get_provider(provider_id: str):
    """Get provider by ID."""
    try:
        with get_db_context() as session:
            provider = session.query(ProviderModel).filter(
                ProviderModel.id == UUID(provider_id)
            ).first()
            
            if not provider:
                return jsonify({"error": "Provider not found"}), 404
            
            return jsonify({
                "id": str(provider.id),
                "name": provider.name,
                "tradeName": provider.trade_name,
                "type": provider.type,
                "status": provider.status,
                "document": provider.document,
                "credentials": provider.credentials,
                "specialties": provider.specialties,
                "phone": provider.phone,
                "email": provider.email,
                "website": provider.website,
                "address": provider.address,
                "workingHours": provider.working_hours,
                "services": provider.services,
                "acceptedInsurers": provider.accepted_insurers,
                "logo": provider.logo,
                "capacity": provider.capacity,
                "hasEmergency": provider.has_emergency,
                "rating": provider.rating,
                "notes": provider.notes,
                "createdAt": provider.created_at.isoformat(),
                "updatedAt": provider.updated_at.isoformat(),
            }), 200
    
    except ValueError:
        return jsonify({"error": "Invalid UUID"}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
