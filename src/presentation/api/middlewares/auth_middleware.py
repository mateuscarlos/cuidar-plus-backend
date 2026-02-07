"""Authentication Middleware."""
from functools import wraps
from flask import request, jsonify
import logging

from src.config import get_settings
from src.infrastructure.security.jwt_handler import JWTHandler

settings = get_settings()
logger = logging.getLogger(__name__)

# Log warning if running in development with auth bypass
if settings.FLASK_ENV == "development":
    logger.warning(
        "⚠️  Authentication bypass enabled in development mode. "
        "All @require_auth routes will accept requests without tokens."
    )


def require_auth(f):
    """
    Decorator to require JWT authentication for a route.
    
    In development mode with FLASK_ENV=development, authentication is bypassed
    and a mock user is injected into the request context.
    
    Usage:
        @app.route('/protected')
        @require_auth
        def protected_route():
            # Access user_id from request context
            user_id = request.user_id
            return jsonify({'user_id': user_id})
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # DEVELOPMENT MODE BYPASS: Skip authentication in development
        if settings.FLASK_ENV == "development":
            # Inject mock user for development
            request.user_id = "00000000-0000-0000-0000-000000000000"
            request.user_email = "dev@cuidar.plus"
            request.user_role = "admin"
            return f(*args, **kwargs)
        
        # PRODUCTION MODE: Require authentication
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return jsonify({"error": "Authorization header is missing"}), 401
        
        try:
            # Extract token from "Bearer <token>"
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != "bearer":
                return jsonify({"error": "Invalid authorization header format"}), 401
            
            token = parts[1]
            
            # Validate token
            jwt_handler = JWTHandler()
            payload = jwt_handler.decode_token(token)
            
            # Check token type
            if payload.get("type") != "access":
                return jsonify({"error": "Invalid token type"}), 401
            
            # Store user info in request context
            request.user_id = payload.get("sub")
            request.user_email = payload.get("email")
            request.user_role = payload.get("role")
            
            return f(*args, **kwargs)
        
        except ValueError as e:
            return jsonify({"error": str(e)}), 401
        except Exception as e:
            return jsonify({"error": "Authentication failed"}), 401
    
    return decorated_function


def require_role(*allowed_roles):
    """
    Decorator to require specific role(s) for a route.
    
    In development mode with FLASK_ENV=development, role checking is bypassed.
    
    Usage:
        @app.route('/admin')
        @require_auth
        @require_role('admin')
        def admin_route():
            return jsonify({'message': 'Admin only'})
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # DEVELOPMENT MODE BYPASS: Skip role checking in development
            if settings.FLASK_ENV == "development":
                return f(*args, **kwargs)
            
            # PRODUCTION MODE: Check user role
            user_role = getattr(request, "user_role", None)
            
            if not user_role:
                return jsonify({"error": "User role not found"}), 403
            
            if user_role not in allowed_roles:
                return jsonify({
                    "error": f"Insufficient permissions. Required roles: {', '.join(allowed_roles)}"
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
