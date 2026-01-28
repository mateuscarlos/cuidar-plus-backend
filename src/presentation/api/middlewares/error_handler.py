"""Error Handler Middleware."""
from flask import jsonify
from werkzeug.exceptions import HTTPException

from src.shared.exceptions.application_exception import ApplicationException
from src.shared.exceptions.domain_exception import DomainException


def register_error_handlers(app):
    """Register error handlers for the Flask app."""
    
    @app.errorhandler(ApplicationException)
    def handle_application_exception(e):
        """Handle application-level exceptions."""
        return jsonify({
            "error": e.message,
            "code": e.code,
        }), 400
    
    @app.errorhandler(DomainException)
    def handle_domain_exception(e):
        """Handle domain-level exceptions."""
        return jsonify({
            "error": e.message,
            "code": "DOMAIN_ERROR",
        }), 400
    
    @app.errorhandler(ValueError)
    def handle_value_error(e):
        """Handle validation errors."""
        return jsonify({
            "error": str(e),
            "code": "VALIDATION_ERROR",
        }), 400
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Handle HTTP exceptions."""
        return jsonify({
            "error": e.description,
            "code": e.name,
        }), e.code
    
    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        """Handle unexpected exceptions."""
        # Log the error (implement logger)
        return jsonify({
            "error": "Internal server error",
            "code": "INTERNAL_ERROR",
        }), 500
