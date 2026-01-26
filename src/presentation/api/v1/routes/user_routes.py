"""User Routes."""
from flask import Blueprint, request, jsonify
from uuid import UUID

from src.application.use_cases.users.create_user import (
    CreateUserInput,
    CreateUserUseCase,
)
from src.application.use_cases.users.get_user_by_id import GetUserByIdUseCase
from src.infrastructure.database.session import get_db_context
from src.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.infrastructure.security.password_hasher import PasswordHasher
from src.shared.exceptions.application_exception import ApplicationException

user_bp = Blueprint("users", __name__, url_prefix="/api/v1/users")


@user_bp.route("/", methods=["POST"])
def create_user():
    """
    Create a new user.
    
    Request body:
    {
        "email": "user@example.com",
        "password": "password123",
        "full_name": "John Doe",
        "role": "caregiver"
    }
    
    Response:
    {
        "id": "...",
        "email": "user@example.com",
        "full_name": "John Doe",
        "role": "caregiver",
        "is_active": true
    }
    """
    try:
        data = request.get_json()
        
        required_fields = ["email", "password", "full_name", "role"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        input_dto = CreateUserInput(
            email=data["email"],
            password=data["password"],
            full_name=data["full_name"],
            role=data["role"],
        )
        
        with get_db_context() as session:
            user_repository = SQLAlchemyUserRepository(session)
            password_hasher = PasswordHasher()
            
            use_case = CreateUserUseCase(user_repository, password_hasher)
            output = use_case.execute(input_dto)
            
            return jsonify({
                "id": str(output.id),
                "email": output.email,
                "full_name": output.full_name,
                "role": output.role,
                "is_active": output.is_active,
            }), 201
    
    except ApplicationException as e:
        return jsonify({"error": e.message, "code": e.code}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@user_bp.route("/", methods=["GET"])
def list_users():
    """
    List all users with pagination.
    """
    try:
        page = request.args.get("page", 1, type=int)
        page_size = request.args.get("pageSize", 20, type=int)
        
        with get_db_context() as session:
            user_repository = SQLAlchemyUserRepository(session)
            
            # Get all users (simplified - you should implement pagination in repository)
            from src.infrastructure.database.models.user_model import UserModel
            users = session.query(UserModel).offset((page - 1) * page_size).limit(page_size).all()
            total = session.query(UserModel).count()
            
            return jsonify({
                "data": [
                    {
                        "id": str(user.id),
                        "name": user.full_name,  # Map full_name to name
                        "email": user.email,
                        "role": user.role.upper(),  # Uppercase to match frontend enum
                        "status": "ACTIVE" if user.is_active else "INACTIVE",  # Map is_active to status
                        "createdAt": user.created_at.isoformat(),
                        "updatedAt": user.updated_at.isoformat(),
                        "lastLogin": user.last_login.isoformat() if user.last_login else None,
                        "permissions": [],  # TODO: Add permissions logic
                        "cpf": "",  # TODO: Add CPF field to user model
                        "phone": "",  # TODO: Add phone field to user model
                    }
                    for user in users
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


@user_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id: str):
    """
    Get user by ID.
    
    Response:
    {
        "id": "...",
        "email": "user@example.com",
        "full_name": "John Doe",
        "role": "caregiver",
        "is_active": true,
        "created_at": "2024-01-01T00:00:00",
        "last_login": "2024-01-15T10:30:00"
    }
    """
    try:
        user_uuid = UUID(user_id)
        
        with get_db_context() as session:
            user_repository = SQLAlchemyUserRepository(session)
            use_case = GetUserByIdUseCase(user_repository)
            output = use_case.execute(user_uuid)
            
            return jsonify({
                "id": str(output.id),
                "email": output.email,
                "full_name": output.full_name,
                "role": output.role,
                "is_active": output.is_active,
                "created_at": output.created_at.isoformat(),
                "last_login": output.last_login.isoformat() if output.last_login else None,
            }), 200
    
    except ValueError:
        return jsonify({"error": "Invalid user ID format"}), 400
    except ApplicationException as e:
        return jsonify({"error": e.message, "code": e.code}), 404
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
