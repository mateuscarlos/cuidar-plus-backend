"""Authentication Routes."""
from flask import Blueprint, request, jsonify

from src.application.use_cases.users.authenticate_user import (
    AuthenticateUserInput,
    AuthenticateUserUseCase,
)
from src.infrastructure.database.session import get_db_context
from src.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.infrastructure.security.password_hasher import PasswordHasher
from src.infrastructure.security.jwt_handler import JWTHandler
from src.shared.exceptions.application_exception import ApplicationException

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate user and return JWT tokens.
    
    Request body:
    {
        "email": "user@example.com",
        "password": "password123"
    }
    
    Response:
    {
        "access_token": "...",
        "refresh_token": "...",
        "token_type": "Bearer",
        "expires_in": 3600
    }
    """
    try:
        data = request.get_json()
        
        if not data or "email" not in data or "password" not in data:
            return jsonify({"error": "Email and password are required"}), 400
        
        input_dto = AuthenticateUserInput(
            email=data["email"],
            password=data["password"],
        )
        
        with get_db_context() as session:
            user_repository = SQLAlchemyUserRepository(session)
            password_hasher = PasswordHasher()
            jwt_handler = JWTHandler()
            
            use_case = AuthenticateUserUseCase(
                user_repository,
                password_hasher,
                jwt_handler,
            )
            
            output = use_case.execute(input_dto)
            
            return jsonify({
                "access_token": output.access_token,
                "refresh_token": output.refresh_token,
                "token_type": output.token_type,
                "expires_in": output.expires_in,
            }), 200
    
    except ApplicationException as e:
        return jsonify({"error": e.message, "code": e.code}), 401
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    """
    Refresh access token using refresh token.
    
    Request body:
    {
        "refresh_token": "..."
    }
    
    Response:
    {
        "access_token": "...",
        "token_type": "Bearer",
        "expires_in": 3600
    }
    """
    try:
        data = request.get_json()
        
        if not data or "refresh_token" not in data:
            return jsonify({"error": "Refresh token is required"}), 400
        
        jwt_handler = JWTHandler()
        
        # Decode and validate refresh token
        payload = jwt_handler.decode_token(data["refresh_token"])
        
        if payload.get("type") != "refresh":
            return jsonify({"error": "Invalid token type"}), 400
        
        # Create new access token
        user_id = payload.get("sub")
        access_token = jwt_handler.create_access_token(subject=user_id)
        
        return jsonify({
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": jwt_handler.access_token_expires,
        }), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
