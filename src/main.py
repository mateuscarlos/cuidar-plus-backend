"""Application Entry Point - Flask App Factory."""
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from src.config import get_settings
from src.presentation.api.middlewares.error_handler import register_error_handlers
from src.presentation.api.v1.routes.auth_routes import auth_bp
from src.presentation.api.v1.routes.inventory_routes import inventory_bp
from src.presentation.api.v1.routes.patient_routes import patient_bp
from src.presentation.api.v1.routes.reports_routes import reports_bp
from src.presentation.api.v1.routes.user_routes import user_bp
from src.shared.utils.logger import app_logger

settings = get_settings()


def create_app() -> Flask:
    """
    Flask Application Factory.

    Creates and configures the Flask application instance.
    """
    app = Flask(__name__)

    # Configuration
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["DEBUG"] = settings.FLASK_ENV == "development"

    # CORS
    CORS(app, origins=settings.get_cors_origins(), supports_credentials=True)

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(reports_bp)

    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health_check():
        """Health check endpoint for monitoring."""
        return jsonify({
            "status": "healthy",
            "service": "cuidar-plus-backend",
            "version": settings.API_VERSION,
        }), 200

    # Root endpoint
    @app.route("/", methods=["GET"])
    def root():
        """Root endpoint with API information."""
        # Content negotiation: Return HTML for browsers, JSON for API clients
        # We list application/json first so that it is preferred for */* (default curl behavior)
        if request.accept_mimetypes.best_match(["application/json", "text/html"]) == "text/html":
            return render_template("landing.html", version=settings.API_VERSION)

        return jsonify({
            "service": "Cuidar Plus API",
            "version": settings.API_VERSION,
            "docs": "/api/docs",
            "health": "/health",
        }), 200

    app_logger.info(f"Flask app created - Environment: {settings.FLASK_ENV}")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=settings.FLASK_ENV == "development")
