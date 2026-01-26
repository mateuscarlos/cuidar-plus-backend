"""Insurer Routes."""
from flask import Blueprint, jsonify, request
from uuid import UUID

from src.application.use_cases.insurers.create_insurer import (
    CreateInsurerInput,
    CreateInsurerUseCase,
)
from src.application.use_cases.insurers.list_insurers import (
    ListInsurersInput,
    ListInsurersUseCase,
)
from src.application.use_cases.insurers.update_insurer import (
    UpdateInsurerInput,
    UpdateInsurerUseCase,
)
from src.infrastructure.database.session import get_db_context
from src.infrastructure.repositories.sqlalchemy_insurer_repository import (
    SQLAlchemyInsurerRepository,
)
from src.shared.exceptions.application_exception import ApplicationException

insurer_bp = Blueprint("insurers", __name__, url_prefix="/api/v1/insurers")


@insurer_bp.route("/", methods=["GET"])
async def list_insurers():
    """
    List insurers with filters.
    
    Query params:
    - search: Search term
    - type: Insurer type
    - status: Insurer status
    - page: Page number (default: 1)
    - pageSize: Page size (default: 50)
    """
    try:
        input_dto = ListInsurersInput(
            search=request.args.get("search"),
            type=request.args.get("type"),
            status=request.args.get("status"),
            has_active_plans=request.args.get("hasActivePlans", type=bool),
            page=request.args.get("page", 1, type=int),
            page_size=request.args.get("pageSize", 50, type=int),
        )
        
        with get_db_context() as session:
            repository = SQLAlchemyInsurerRepository(session)
            use_case = ListInsurersUseCase(repository)
            output = await use_case.execute(input_dto)
            
            return jsonify({
                "data": [
                    {
                        "id": str(item.id),
                        "name": item.name,
                        "tradeName": item.trade_name,
                        "cnpj": item.cnpj,
                        "type": item.type,
                        "status": item.status,
                        "phone": item.phone,
                        "email": item.email,
                    }
                    for item in output.items
                ],
                "pagination": {
                    "total": output.total,
                    "page": output.page,
                    "pageSize": output.page_size,
                    "totalPages": (output.total + output.page_size - 1) // output.page_size,
                }
            }), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@insurer_bp.route("/", methods=["POST"])
async def create_insurer():
    """
    Create a new insurer.
    
    Request body:
    {
        "name": "Sul América Seguros",
        "tradeName": "Sul América",
        "cnpj": "12.345.678/0001-90",
        "registrationNumber": "123456",
        "type": "MEDICINA_GRUPO",
        "phone": "(11) 3000-0000",
        "email": "contato@sulamerica.com.br",
        "website": "https://www.sulamerica.com.br",
        "address": {
            "street": "Av. Paulista",
            "number": "1000",
            "complement": "10º andar",
            "neighborhood": "Bela Vista",
            "city": "São Paulo",
            "state": "SP",
            "zipCode": "01310-100"
        },
        "logo": "https://...",
        "notes": "..."
    }
    """
    try:
        data = request.get_json()
        
        required_fields = [
            "name", "tradeName", "cnpj", "registrationNumber", "type",
            "phone", "email", "address"
        ]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        input_dto = CreateInsurerInput(
            name=data["name"],
            trade_name=data["tradeName"],
            cnpj=data["cnpj"],
            registration_number=data["registrationNumber"],
            type=data["type"],
            phone=data["phone"],
            email=data["email"],
            address=data["address"],
            website=data.get("website"),
            logo=data.get("logo"),
            notes=data.get("notes"),
        )
        
        with get_db_context() as session:
            repository = SQLAlchemyInsurerRepository(session)
            use_case = CreateInsurerUseCase(repository)
            output = await use_case.execute(input_dto)
            
            return jsonify({
                "id": str(output.id),
                "name": output.name,
                "tradeName": output.trade_name,
                "cnpj": output.cnpj,
                "status": output.status,
            }), 201
    
    except ApplicationException as e:
        return jsonify({"error": e.message, "code": e.code}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@insurer_bp.route("/<insurer_id>", methods=["GET"])
async def get_insurer(insurer_id: str):
    """Get insurer by ID."""
    try:
        with get_db_context() as session:
            repository = SQLAlchemyInsurerRepository(session)
            insurer = await repository.get_by_id(UUID(insurer_id))
            
            if not insurer:
                return jsonify({"error": "Insurer not found"}), 404
            
            return jsonify({
                "id": str(insurer.id),
                "name": insurer.name,
                "tradeName": insurer.trade_name,
                "cnpj": insurer.cnpj,
                "registrationNumber": insurer.registration_number,
                "type": insurer.type.value,
                "status": insurer.status.value,
                "phone": insurer.phone,
                "email": insurer.email,
                "website": insurer.website,
                "address": {
                    "street": insurer.address.street,
                    "number": insurer.address.number,
                    "complement": insurer.address.complement,
                    "neighborhood": insurer.address.neighborhood,
                    "city": insurer.address.city,
                    "state": insurer.address.state,
                    "zipCode": insurer.address.zip_code,
                },
                "plans": [
                    {
                        "id": str(plan.id),
                        "name": plan.name,
                        "code": plan.code,
                        "type": plan.type.value,
                        "coverage": plan.coverage,
                        "active": plan.active,
                        "monthlyPrice": plan.monthly_price,
                    }
                    for plan in insurer.plans
                ],
                "logo": insurer.logo,
                "contractStartDate": insurer.contract_start_date.isoformat() if insurer.contract_start_date else None,
                "contractEndDate": insurer.contract_end_date.isoformat() if insurer.contract_end_date else None,
                "notes": insurer.notes,
                "createdAt": insurer.created_at.isoformat(),
                "updatedAt": insurer.updated_at.isoformat(),
            }), 200
    
    except ValueError:
        return jsonify({"error": "Invalid UUID"}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@insurer_bp.route("/<insurer_id>", methods=["PUT"])
async def update_insurer(insurer_id: str):
    """Update an insurer."""
    try:
        data = request.get_json()
        
        input_dto = UpdateInsurerInput(
            id=UUID(insurer_id),
            name=data.get("name"),
            trade_name=data.get("tradeName"),
            phone=data.get("phone"),
            email=data.get("email"),
            website=data.get("website"),
            status=data.get("status"),
            logo=data.get("logo"),
            notes=data.get("notes"),
        )
        
        with get_db_context() as session:
            repository = SQLAlchemyInsurerRepository(session)
            use_case = UpdateInsurerUseCase(repository)
            output = await use_case.execute(input_dto)
            
            return jsonify({
                "id": str(output.id),
                "name": output.name,
                "status": output.status,
            }), 200
    
    except ApplicationException as e:
        return jsonify({"error": e.message, "code": e.code}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@insurer_bp.route("/<insurer_id>", methods=["DELETE"])
async def delete_insurer(insurer_id: str):
    """Delete an insurer."""
    try:
        with get_db_context() as session:
            repository = SQLAlchemyInsurerRepository(session)
            success = await repository.delete(UUID(insurer_id))
            
            if not success:
                return jsonify({"error": "Insurer not found"}), 404
            
            return jsonify({"message": "Insurer deleted successfully"}), 200
    
    except ValueError:
        return jsonify({"error": "Invalid UUID"}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
